import frappe
from frappe import _


@frappe.whitelist(allow_guest=False)
def confirm_parcels_in_wr(doc):
    """ Used as Action button in Doctype: Confirm the receipt of the parcels. Change status to: "Awaiting Departure" """
    # TODO: Make this some sort or generic def, to change status across multiple statuses
    doc = frappe.parse_json(doc)

    updated_docs = 0
    wr_lines, wr_lines_len = doc.warehouse_receipt_lines, len(doc.warehouse_receipt_lines)

    # Core: Silence Notifications and emails!
    frappe.flags.mute_emails = frappe.flags.in_import = doc.mute_emails

    for i, wr_line in enumerate(wr_lines, start=1):
        progress = i * 100 / wr_lines_len

        parcel = frappe.get_doc('Parcel', wr_line['parcel'])  # Getting Parcel Doctype

        if parcel.change_status('Awaiting Departure'):  # If Status can be changed. To prevent unnecessary updates
            updated_docs += 1
            parcel.flags.ignore_validate = True  # Set flag ON because Doc will be saved from bulk edit. No validations.
            parcel.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

        # TODO: Fix, after publish progress: CTL+S is not working.
        frappe.publish_progress(
            percent=progress, title=_('Confirming Parcels'),
            description=_('Confirming Parcel {0}').format(parcel.tracking_number),
        )

    frappe.flags.mute_emails = frappe.flags.in_import = False  # Reset core flags.

    frappe.msgprint(msg='{0} Parcels confirmed of {1}.'.format(updated_docs, wr_lines_len), title=_('Success'))
