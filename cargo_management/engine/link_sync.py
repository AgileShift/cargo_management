from dataclasses import dataclass

import frappe
from frappe import _

from cargo_management.engine.utils import pluck_child_field


@dataclass(frozen=True)
class LinkSyncRule:
	child_table: str
	child_link_field: str
	target_doctype: str
	target_link_field: str
	allow_duplicate_links: bool = False


class LinkSyncMixin:
	link_sync_rules: tuple[LinkSyncRule, ...] = ()

	def validate_link_sync(self):
		for rule in self.link_sync_rules:
			target_names = pluck_child_field(self.get(rule.child_table), rule.child_link_field)
			if not rule.allow_duplicate_links:
				self._validate_duplicate_links(rule, target_names)
			self._validate_existing_links(rule, target_names)

	def capture_link_sync_state(self):
		self._previous_link_sync_names = {
			rule: self._get_previous_link_names(rule)
			for rule in self.link_sync_rules
		}

	def sync_links(self):
		for rule in self.link_sync_rules:
			current_names = set(pluck_child_field(self.get(rule.child_table), rule.child_link_field))
			previous_names_by_rule = getattr(self, "_previous_link_sync_names", {})
			previous_names = previous_names_by_rule.get(rule, self._get_previous_link_names(rule))

			for target_name in current_names:
				if frappe.db.get_value(rule.target_doctype, target_name, rule.target_link_field) != self.name:
					frappe.db.set_value(
						rule.target_doctype,
						target_name,
						rule.target_link_field,
						self.name,
						update_modified=False,
					)

			self._clear_removed_links(rule, previous_names - current_names)

	def unlink_synced_links(self):
		for rule in self.link_sync_rules:
			target_names = set(pluck_child_field(self.get(rule.child_table), rule.child_link_field))
			self._clear_removed_links(rule, target_names)

	def _get_previous_link_names(self, rule):
		doc_before_save = self.get_doc_before_save()

		if not doc_before_save:
			return set()

		return set(pluck_child_field(doc_before_save.get(rule.child_table), rule.child_link_field))

	def _clear_removed_links(self, rule, target_names):
		for target_name in target_names:
			if frappe.db.get_value(rule.target_doctype, target_name, rule.target_link_field) == self.name:
				frappe.db.set_value(
					rule.target_doctype,
					target_name,
					rule.target_link_field,
					None,
					update_modified=False,
				)

	def _validate_duplicate_links(self, rule, target_names):
		seen, duplicates = set(), set()

		for target_name in target_names:
			if target_name in seen:
				duplicates.add(target_name)
			seen.add(target_name)

		if duplicates:
			frappe.throw(
				msg=[
					_("{0} {1} appears more than once.").format(rule.target_doctype, frappe.bold(target_name))
					for target_name in sorted(duplicates)
				],
				title=_("Duplicate {0}").format(rule.target_doctype),
				as_list=True,
			)

	def _validate_existing_links(self, rule, target_names):
		conflicts = []

		for target_name in set(target_names):
			current_link = frappe.db.get_value(rule.target_doctype, target_name, rule.target_link_field)
			if current_link and current_link != self.name:
				conflicts.append((target_name, current_link))

		if conflicts:
			frappe.throw(
				msg=[
					_("{0} {1} is already linked to {2}.").format(
						rule.target_doctype,
						frappe.bold(target_name),
						frappe.bold(current_link),
					)
					for target_name, current_link in sorted(conflicts)
				],
				title=_("{0} Already Linked").format(rule.target_doctype),
				as_list=True,
			)
