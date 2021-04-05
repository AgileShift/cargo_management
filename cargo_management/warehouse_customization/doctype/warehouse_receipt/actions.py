import frappe
from cargo_management.package_management.doctype.package.utils import get_field_list_from_child_table, change_status
from frappe import _


@frappe.whitelist()
def update_status(doc, new_status: str):
    doc = frappe.parse_json(doc)  # Getting the Warehouse Receipt Doc.

    change_status(docs_to_update={
        'Package': {
            'new_status': new_status,
            'doc_names': get_field_list_from_child_table(doc.get('warehouse_receipt_lines'), 'package'),
            'updated': 0  # FIXME: find a way to dont send this
        }
    }, title=_('Confirm Packages'), mute_emails=doc.mute_emails)

    # for i, wr_line in enumerate(doc.warehouse_receipt_lines, start=1):
    #     progress = i * 100 / len(doc.warehouse_receipt_lines)

        # TODO: Fix, after publish progress: CTL+S is not working.
        # frappe.publish_progress(
        #     percent=progress, title='Confirming Packages',
        #     description='Confirming Package {0}'.format(package.tracking_number),
        # )
#36 original
#16 lineas, despues de refactorizar