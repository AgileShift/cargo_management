import frappe
from cargo_management.package_management.doctype.package.utils import get_field_list_from_child_table, change_status
from frappe import _


@frappe.whitelist()
def update_status(source_doc_name: str, new_status: str):
    doc = frappe.get_doc('Cargo Shipment', source_doc_name)  # Getting the Cargo Shipment Doc.

    # FIXME: This is provisional, maybe we can add packages as a child table of Cargo Shipment
    packages_in_warehouse_receipts = []
    for cs_line in doc.get('cargo_shipment_lines'):  # This actual lines are references for Warehouse Receipt
        wr = frappe.get_doc('Warehouse Receipt', cs_line.warehouse_receipt)  # Getting Warehouse Receipt

        packages_in_warehouse_receipts.extend(
            get_field_list_from_child_table(wr.warehouse_receipt_lines, 'package')  # Getting all package names from wr
        )

    change_status(docs_to_update={
        'Cargo Shipment': {
            'doc_names': [doc.name]
        },
        'Warehouse Receipt': {
            'doc_names': get_field_list_from_child_table(doc.get('cargo_shipment_lines'), 'warehouse_receipt')
        },
        'Package': {
            'doc_names': packages_in_warehouse_receipts
        }
    }, new_status=new_status, msg_title=_('Now in Transit'), mute_emails=doc.mute_emails)
