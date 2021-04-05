# TODO: Maybe we can move this to a module?
import frappe


def get_field_list_from_child_table(child_lines: list, field: str):
    """ This takes a List of Dicts [{}] and return a List of values. """
    return list(map(lambda child_line: child_line.get(field), child_lines))


def change_status(docs_to_update: dict, new_status=None, msg_title: str = '', mute_emails=True):
    """ This tries to update all docs statuses, no matter what doctype is. """
    message = []  # For Gathering Message.

    """ TODO
    for i, wr_line in enumerate(doc.warehouse_receipt_lines, start=1):
        progress = i * 100 / len(doc.warehouse_receipt_lines)

    # TODO: Fix, after publish progress: CTL+S is not working.
    frappe.publish_progress(
        percent=progress, title='Confirming Packages',
        description='Confirming Package {0}'.format(package.tracking_number),
    ) """

    frappe.flags.mute_emails = frappe.flags.in_import = mute_emails  # Core: Silence all notifications and emails.

    for doctype, opts in docs_to_update.items():  # Iterate all over Doctypes
        updated_docs = 0                          # Reset Updated Docs Counter to zero each time we change of doctype

        for name in opts['doc_names']:            # Iterate all over docs to update
            doc = frappe.get_doc(doctype, name)   # Getting Doc from current Doctype

            if doc.change_status(opts.get('new_status', new_status)):  # If status can be changed. Prevent unnecessary updates
                updated_docs += 1                  # Add to updated docs
                doc.flags.ignore_validate = True   # Set flag ON because Doc will be saved from bulk edit. No validations
                doc.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

        # Creating Message to show as result of this Iteration
        message.append('{updated} out of {total} {doctype}s have been updated to {new_status}.'.format(
            updated=updated_docs, total=len(opts['doc_names']), doctype=doctype, new_status=opts.get('new_status', new_status)
        ))

    frappe.flags.mute_emails = frappe.flags.in_import = False  # Core: Reset all notifications and emails.

    frappe.msgprint(msg=message, title=msg_title, as_list=True, indicator='green')  # Show message as dialog
