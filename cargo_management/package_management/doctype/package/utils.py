# TODO: Maybe we can move this to a module?
import frappe


def get_field_list_from_child_table(child_lines: list, field: str):
    """ This takes a List of Dicts [{}] and return a List of values. """
    return list(map(lambda child_line: child_line.get(field), child_lines))


def change_status(docs_to_update: dict, title: str, mute_emails=True):
    """ This tries to update all docs statuses, no matter what doctype is. """
    message = []  # For Gathering Message and Title

    frappe.flags.mute_emails = frappe.flags.in_import = mute_emails  # Core: Silence all notifications and emails.

    for doctype, opts in docs_to_update.items():  # Iterate all over Doctypes
        for name in opts['doc_names']:            # Iterate all over docs to update
            doc = frappe.get_doc(doctype, name)   # Getting Doc from current Doctype

            if doc.change_status(opts['new_status']):    # If status can be changed. Prevent unnecessary updates
                opts['updated'] += 1                     # Add to updated counter
                doc.flags.ignore_validate = True         # Set flag ON because Doc will be saved from bulk edit. No validations
                # package.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

        # Creating Message to show as result of this Iteration
        message.append('{updated} out of {total} {doctype}s have been updated to {new_status}.'.format(
            updated=opts['updated'], total=len(opts['doc_names']), doctype=doctype, new_status=opts['new_status']
        ))

    frappe.flags.mute_emails = frappe.flags.in_import = False  # Core: Reset all notifications and emails.

    frappe.msgprint(msg=message, title=title, as_list=True, indicator='green')  # Show message as dialog
#31 lineas y ya casi funciona
# 79 lineas en codigo separado