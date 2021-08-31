import frappe
from cargo_management.utils import get_list_from_child_table, update_status_in_bulk
from frappe import _


@frappe.whitelist()
def update_status(source_doc_name: str, new_status: str):
    doc = frappe.get_cached_doc('Cargo Shipment', source_doc_name)  # Getting the Cargo Shipment Doc from db

    wrs_in_cs = get_list_from_child_table(doc.cargo_shipment_lines, 'warehouse_receipt')
    packages_in_cs = frappe.get_all('Warehouse Receipt Line', fields='package', filters={'parent': ['in', wrs_in_cs]}, pluck='package')

    update_status_in_bulk(docs_to_update={
        'Cargo Shipment': [doc.name],
        'Warehouse Receipt': wrs_in_cs,
        'Package': packages_in_cs
    }, new_status=new_status, msg_title=_('Now in Transit'), mute_emails=doc.mute_emails)
