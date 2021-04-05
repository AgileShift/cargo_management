import frappe
from cargo_management.package_management.doctype.package.utils import get_field_list_from_child_table, change_status
from frappe import _


@frappe.whitelist()
def update_status(doc, new_status: str):
    doc = frappe.parse_json(doc)  # Getting the Warehouse Receipt Doc.

    change_status(docs_to_update={
        'Package': {
            'doc_names': get_field_list_from_child_table(doc.get('warehouse_receipt_lines'), 'package'),
        }
    }, new_status=new_status, msg_title=_('Confirm Packages'), mute_emails=doc.mute_emails)
