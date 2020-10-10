import frappe
import json


def get_parcels_in_warehouse_receipt(warehouse_receipt=None, warehouse_receipt_lines=None):

    if warehouse_receipt_lines:  # Get the parcels using the receipt lines
        print('Using Warehouse Receipt Lines')

        if type(warehouse_receipt_lines) is list:
            parcels_in_wr = ', '.join(line['parcel'] for line in warehouse_receipt_lines)

            parcels = frappe.get_all('Parcel', filters=[('name', 'in', parcels_in_wr)], fields=['name', 'status'])

    return parcels


@frappe.whitelist(allow_guest=False)
def manual_confirm_parcels(doc):
    """ Confirms the receipt of the parcels. """
    doc = json.loads(doc)

    wr_lines = doc.get('warehouse_receipt_lines')
    wr_lines_len = len(wr_lines)

    real_number_of_updated_doc = 0

    for i, wr_line in enumerate(wr_lines, start=1):
        progress = float(i) * 100 / wr_lines_len

        parcel = frappe.get_doc('Parcel', wr_line['parcel'])
        able_to_change, message = parcel.can_change_status('Awaiting Dispatch')

        if able_to_change:
            real_number_of_updated_doc += 1

            if doc.get('mute_emails'):
                print('Mutting emails')
                parcel.set()
            else:
                parcel.db_set('status', 'Awaiting Departure', update_modified=False)

        frappe.publish_progress(
            percent=progress, title='Confirming Parcels', doctype='Parcel', docname=parcel.name,
            description='Confirming Parcel {0}'.format(parcel.tracking_number)
        )

    frappe.msgprint(msg='{0} Parcels confirmed of {1}.'.format(real_number_of_updated_doc, wr_lines_len), title='Success')
