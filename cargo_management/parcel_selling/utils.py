import frappe


def sales_invoice_on_submit(doc, method):
	""" Change status of package after submit. """

	# TODO: Avoid duplicate tracking
	for item in doc.items:  # Iter over all items on sales invoice
		parcel = frappe.get_doc('Parcel', item.package)

		if parcel.change_status('Unpaid'):  # If it can change status
			# Set flag ON because Doc will be saved from bulk edit. No validations
			parcel.save(ignore_permissions=True)  # , ignore_validate=True)  # Trigger before_save() who checks for the flag


def sales_invoice_on_update_after_submit(doc, method):
	""" Change status of package after submit. """
	# THIS is a HOTFIX: Not recommended way. The hook is for 'on_change'
	if doc.status != 'Paid':
		return

	for item in doc.items:  # Iter over all items on sales invoice
		package = frappe.get_doc('Parcel', item.package)

		if package.change_status('For Delivery or Pickup'):  # If it can change status
			# Set flag ON because Doc will be saved from bulk edit. No validations
			package.save(ignore_permissions=True)  # , ignore_validate=True)  # Trigger before_save() who checks for the flag
