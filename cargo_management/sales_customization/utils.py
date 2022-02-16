import frappe


def sales_invoice_on_submit(doc, method):
    """ Change status of package after submit. """

    # TODO: Avoid duplicate tracking
    for item in doc.items:  # Iter over all items on sales invoice
        package = frappe.get_doc('Package', item.package)

        if package.change_status('Unpaid'):  # If it can change status
            # Set flag ON because Doc will be saved from bulk edit. No validations
            package.save(ignore_permissions=True, ignore_validate=True)  # Trigger before_save() who checks for the flag
