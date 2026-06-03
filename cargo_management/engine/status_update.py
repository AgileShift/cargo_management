from dataclasses import dataclass

import frappe
from frappe import _

from cargo_management.engine.utils import pluck_child_field


@dataclass
class StatusUpdateTarget:
	doctype: str
	doc_names: list[str]
	new_status: str | None = None


class BulkStatusUpdate:
	def __init__(self, new_status=None, msg_title=""):
		self.new_status = new_status
		self.msg_title = msg_title
		self.targets: list[StatusUpdateTarget] = []

	def include_doc(self, doctype, doc_name, new_status=None):
		return self.include(doctype, [doc_name], new_status)

	def include_child_links(self, doctype, child_rows, fieldname, new_status=None):
		return self.include(doctype, pluck_child_field(child_rows, fieldname), new_status)

	def include(self, doctype, doc_names, new_status=None):
		doc_names = list(dict.fromkeys(name for name in doc_names or [] if name))
		if doc_names:
			self.targets.append(StatusUpdateTarget(doctype, doc_names, new_status))
		return self

	def run(self):
		total_docs = sum(len(target.doc_names) for target in self.targets)
		if not total_docs:
			return []

		messages, current_doc = [], 0

		for target in self.targets:
			updated_docs = 0
			target_status = target.new_status or self.new_status

			for doc_name in target.doc_names:
				doc = frappe.get_doc(target.doctype, doc_name)

				if doc.change_status(target_status):
					updated_docs += 1
					doc.flags.ignore_validate = True
					doc.save(ignore_permissions=True)

				current_doc += 1
				frappe.publish_progress(
					percent=(current_doc / total_docs * 100),
					title=self.msg_title,
					description=f"Updating Status to {target.doctype}: {doc_name}",
				)

			messages.append(
				f"{updated_docs} out of {len(target.doc_names)} {target.doctype}s have been updated to {target_status}."
			)

		frappe.msgprint(msg=messages, title=self.msg_title, as_list=True, indicator="green")
		return messages


@frappe.whitelist(methods="POST")
def update_cargo_shipment_status(source_doc_name: str, new_status: str, msg_title: str):
	doc = frappe.get_cached_doc("Cargo Shipment", source_doc_name)

	(
		BulkStatusUpdate(new_status=new_status, msg_title=msg_title)
		.include_doc("Cargo Shipment", doc.name)
		.include_child_links("Warehouse Receipt", doc.cargo_shipment_lines, "warehouse_receipt")
		.include_child_links("Parcel", doc.cargo_shipment_lines, "parcel")
		.run()
	)


@frappe.whitelist(methods="POST")
def update_cargo_shipment_receipt_status(source_doc_name: str, new_status: str):
	doc = frappe.get_cached_doc("Cargo Shipment Receipt", source_doc_name)
	cargo_shipment = frappe.get_doc("Cargo Shipment", doc.cargo_shipment)

	(
		BulkStatusUpdate(new_status=new_status, msg_title=_("Marked as Sorting"))
		.include_doc("Cargo Shipment Receipt", doc.name)
		.include_doc("Cargo Shipment", doc.cargo_shipment)
		.include_child_links("Warehouse Receipt", cargo_shipment.cargo_shipment_lines, "warehouse_receipt")
		.include_child_links("Parcel", doc.cargo_shipment_receipt_lines, "parcel")
		.run()
	)
