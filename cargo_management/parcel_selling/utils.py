import frappe


def sales_invoice_on_submit(doc, method):
	""" Change the status of the package after submitting. """

	# TODO: Avoid duplicate tracking
	for item in doc.items:  # Iter over all items on sales invoice
		if item.package is None:
			return

		parcel = frappe.get_doc('Parcel', item.package)

		if parcel.change_status('Unpaid'):  # If it can change status
			# Set flag ON because Doc will be saved from bulk edit. No validations
			parcel.save(ignore_permissions=True)  # , ignore_validate=True)  # Trigger before_save() who checks for the flag


def sales_invoice_on_update_after_submit(doc, method):
	""" Change the status of the package after submitting. """
	# FIXME: THIS is a HOTFIX: Not recommended way. The hook is for 'on_change'
	if doc.status != 'Paid':
		return

	for item in doc.items:  # Iter over all items on sales invoice
		if item.package is None:
			return

		parcel = frappe.get_doc('Parcel', item.package)

		if parcel.change_status('For Delivery or Pickup'):  # If it can change status
			# Set flag ON because Doc will be saved from bulk edit. No validations
			parcel.save(ignore_permissions=True)  # , ignore_validate=True)  # Trigger before_save() who checks for the flag
