import frappe
from cargo_management.utils import get_list_from_child_table, update_status_in_bulk


@frappe.whitelist(methods='POST')
def update_status(source_doc_name: str, new_status: str, msg_title: str):
    doc = frappe.get_cached_doc('Cargo Shipment', source_doc_name)  # Getting the Cargo Shipment Doc from db

    wrs_in_cs = get_list_from_child_table(doc.cargo_shipment_lines, 'warehouse_receipt')  # TODO: Filter Unique
    packages_in_cs = get_list_from_child_table(doc.cargo_shipment_lines, 'package')

    update_status_in_bulk(docs_to_update={
        'Cargo Shipment': [doc.name],
        'Warehouse Receipt': wrs_in_cs,
        'Parcel': packages_in_cs
    }, new_status=new_status, msg_title=msg_title, mute_emails=doc.mute_emails)  # todo: Work on msg_title
