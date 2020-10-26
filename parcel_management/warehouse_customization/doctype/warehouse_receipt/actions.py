import frappe


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
    doc = frappe.parse_json(doc)

    wr_lines = doc.get('warehouse_receipt_lines')
    wr_lines_len = len(wr_lines)
    updated_docs = 0

    frappe.flags.mute_emails, frappe.flags.in_import = True, True

    for i, wr_line in enumerate(wr_lines, start=1):
        progress = float(i) * 100 / wr_lines_len

        parcel = frappe.get_doc('Parcel', wr_line['parcel'])

        if parcel.change_status('Awaiting Dispatch'):

            updated_docs += 1
            frappe.flags.mute_emails, frappe.flags.in_import = True, True

            parcel.flags.ignore_validate = True  # Set flag ON because Doc will be saved from bulk edit. No validations.
            parcel.save()
            # if doc.get('mute_emails'):  # TODO: How to mute emails of status changes?

        print(progress)
        frappe.publish_progress(
            percent=progress, title='Confirming Parcels', #doctype='Warehouse Receipt', docname=doc.name,
            description='Confirming Parcel {0}.'.format(parcel.tracking_number)
        )

    print('   ')

    # frappe.msgprint(msg='{0} Parcels confirmed of {1}.'.format(updated_docs, wr_lines_len), title='Success')
