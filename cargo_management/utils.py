import datetime

import pytz

import frappe


def get_list_from_child_table(child_lines: list, field: str):
	""" This takes a List of Dicts [{}] and return a List of Uniques values. """
	return list(set(child_line.get(field) for child_line in child_lines if child_line.get(field)))  # FIXME: Performance?


# https://github.com/frappe/frappe/pull/23414
def update_status_in_bulk(docs_to_update: dict, new_status: str = None, msg_title: str = '', mute_emails: bool = True):
	"""
	This tries to update all docs statuses, no matter what doctype is.

	@param docs_to_update: {'Doctype': [names] } or { 'Doctype': {'doc_names': [names], 'new_status': 'string' } }
	@param new_status: str. To be used in Doctype where new status was not explicitly declared in docs_to_update dict
	@param msg_title: str. Title for the dialog
	@param mute_emails: bool. This activates or deactivates notifications on backend. True if not sent
	"""
	message, iter_doc = [], 0  # For Gathering Message, counter of current iter of all doc_names
	total_doc_names = sum(len(docs) if type(docs) is list else len(docs['doc_names']) for docs in docs_to_update.values())

	frappe.flags.mute_emails = frappe.flags.in_import = mute_emails  # Core: Silence all notifications and emails.

	for doctype, opts in docs_to_update.items():  # Iterate all over Doctypes. opts can be: Dict or List.
		updated_docs = 0  # Reset Updated Docs Counter to zero each time we change of Doctype.

		try:  # if opts is a Dict -> {'doc_names': [doc_names], 'new_status': 'string' }
			doc_names, doc_new_status = opts['doc_names'], opts.get('new_status', new_status)  # if no status is passed
		except TypeError:  # if opts is a List. We use default new_status from def params
			doc_names, doc_new_status = opts, new_status

		for name in doc_names:  # Iterate all over docs to update
			doc = frappe.get_doc(doctype, name)  # Getting Doc from current DocType

			if doc.change_status(doc_new_status):  # If status can be changed. Prevent unnecessary updates
				updated_docs += 1  # Count, because this document could be updated
				doc.flags.ignore_validate = True  # Set flag ON because Doc will be saved from bulk edit. No validations
				doc.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

			iter_doc += 1  # Count each time we iter a doc to change. We don't reset soo we can count all DocTypes.
			frappe.publish_progress(  # TODO: Sometimes this dont get to 100%
				percent=(iter_doc / total_doc_names * 100), title=msg_title,  # doctype=doctype, docname=name,
				description='Updating Status to {doctype}: {doc_name}'.format(doctype=doctype, doc_name=name)
			)

		# Creating Message to show with results of status change to doctype
		message.append('{updated} out of {total} {doctype}s have been updated to {new_status}.'.format(
			updated=updated_docs, total=len(doc_names), doctype=doctype, new_status=doc_new_status
		))

	frappe.flags.mute_emails = frappe.flags.in_import = False  # Core: Reset all notifications and emails.

	frappe.msgprint(msg=message, title=msg_title, as_list=True, indicator='green')  # Show message as dialog


# TODO: Validate if needed
def naive_dt_to_local_dt(dt_str: str, uses_utc: bool):
	if not dt_str:  # Sometimes datetime string if empty for some values, so return None value.
		return

	# Parse datetime from string; At this moment we don't know if it's in UTC or local.
	naive_datetime = datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S%z')

	if not uses_utc:  # API already give us local datetime. So no need to convert from UTC to local
		return naive_datetime.replace(tzinfo=None)

	# TODO: Make this conversion warehouse location aware!. For now we're pretending only Miami is local timezone
	local_tz = pytz.timezone('America/New_York')  # https://stackoverflow.com/a/32313111/3172310

	# Return unaware local datetime: Converts unaware UTC datetime to aware UTC and then delete the timezone info.
	return naive_datetime.astimezone(tz=local_tz).replace(tzinfo=None)
