import frappe
from cargo_management.utils import get_list_from_child_table, change_status
from frappe import _


@frappe.whitelist()
def update_status(source_doc_name: str, new_status: str):
    # It is more safe to get the doc from db that receive it from client-side as param
    doc = frappe.get_cached_doc('Warehouse Receipt', source_doc_name)  # Getting the Warehouse Receipt Doc from db

    change_status(docs_to_update={
        'Package': get_list_from_child_table(doc.warehouse_receipt_lines, 'package')
    }, new_status=new_status, msg_title=_('Confirm Packages'), mute_emails=doc.mute_emails)
