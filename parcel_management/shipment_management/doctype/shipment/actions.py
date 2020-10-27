import frappe


@frappe.whitelist(allow_guest=False)
def mark_shipment_in_transit(doc):
    """ Used as Action button in Doctype: Change status of the parcels and the warehouses receipts of the shipment. """
    doc = frappe.parse_json(doc)

    for shipment_line in doc.shipment_lines:
        warehouse_receipt = frappe.get_doc('Warehouse Receipt', shipment_line.get('warehouse_receipt'))

        # TODO: Optimize, one single query to alter all statuses.
        # frappe.db.set_value('Warehouse Receipt', shipment_line.get('warehouse_receipt'), 'status', 'CLOSED')

        for wr_receipt_line in warehouse_receipt.warehouse_receipt_lines:
            frappe.db.set_value('Parcel', wr_receipt_line.get('parcel'), 'status', 'Finished')
