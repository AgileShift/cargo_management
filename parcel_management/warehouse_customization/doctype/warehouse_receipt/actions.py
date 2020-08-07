import frappe
import json


@frappe.whitelist(allow_guest=False)
def manual_confirm_parcels(doc):
    """ Confirms the receipt of the parcels. """
    doc = json.loads(doc)

    for receipt_line in doc.get('warehouse_receipt_lines'):
        # TODO: Optimize, one single query to alter all statuses.
        frappe.db.set_value('Parcel', receipt_line.get('parcel'), 'status', 'waiting_for_departure')
