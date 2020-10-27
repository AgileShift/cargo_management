import frappe

# TODO: Delete this?
def get_parcels_in_warehouse_receipt(warehouse_receipt=None, warehouse_receipt_lines=None):

    if warehouse_receipt_lines:  # Get the parcels using the receipt lines
        print('Using Warehouse Receipt Lines')

        if type(warehouse_receipt_lines) is list:
            parcels_in_wr = ', '.join(line['parcel'] for line in warehouse_receipt_lines)

            parcels = frappe.get_all('Parcel', filters=[('name', 'in', parcels_in_wr)], fields=['name', 'status'])

    return parcels


@frappe.whitelist(allow_guest=False)
def confirm_parcels(doc):
    """ Used as Action button in Doctype: Confirms the receipt of the parcels. Change status to: "Awaiting Dispatch" """
    # TODO: Make this some sort or generic def, to change status across multiple statuses
    doc = frappe.parse_json(doc)

    wr_lines = doc.warehouse_receipt_lines  # Getting all the Parcels
    wr_lines_len = len(wr_lines)
    updated_docs = 0

    # Core: Silence Notifications and emails!
    frappe.flags.mute_emails, frappe.flags.in_import = doc.mute_emails, doc.mute_emails

    for i, wr_line in enumerate(wr_lines, start=1):
        progress = i * 100 / wr_lines_len

        parcel = frappe.get_doc('Parcel', wr_line['parcel'])  # Getting Parcel Doctype

        if parcel.change_status('Awaiting Dispatch'):  # If Status can be changed
            updated_docs += 1
            parcel.flags.ignore_validate = True  # Set flag ON because Doc will be saved from bulk edit. No validations.
            parcel.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

        # TODO: Fix, after publish progress: CTL+S is not working.
        frappe.publish_progress(
            percent=progress, title='Confirming Parcels',
            description='Confirming Parcel {0}.'.format(parcel.tracking_number),
        )

    frappe.flags.mute_emails, frappe.flags.in_import = False, False  # Reset core flags.

    frappe.msgprint(msg='{0} Parcels confirmed of {1}.'.format(updated_docs, wr_lines_len), title='Success')
