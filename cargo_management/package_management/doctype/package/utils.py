# TODO: Maybe we can move this to a module?
import frappe


def get_list_from_child_table(child_lines: list, field: str):
    """ This takes a List of Dicts [{}] and return a List of values. """
    return list(map(lambda child_line: child_line.get(field), child_lines))


def change_status(docs_to_update: dict, new_status: str = None, msg_title: str = '', mute_emails: bool = True):
    """
    This tries to update all docs statuses, no matter what doctype is.

    @param docs_to_update: {'Doctype': [doc_names] or {'doc_names': [doc_names], 'new_status': 'string' } }
    @param new_status: str. To be used in doctypes where new status was not explicitly declared in docs_to_update dict
    @param msg_title: str. Title for the dialog
    @param mute_emails: bool. This activate or deactivates notifications on backend. True if not sent
    """
    message, iter_doc = [], 0  # For Gathering Message, counter of current iter of all doc_names
    total_doc_names = sum(len(docs) if type(docs) == list else len(docs['doc_names']) for docs in docs_to_update.values())

    frappe.flags.mute_emails = frappe.flags.in_import = mute_emails  # Core: Silence all notifications and emails.

    for doctype, opts in docs_to_update.items():  # Iterate all over Doctypes. opts can be: dict or list.
        updated_docs = 0                          # Reset Updated Docs Counter to zero each time we change of doctype.

        try:  # If opts is a dict -> {'doc_names': [doc_names], 'new_status': 'string' }
            doc_names, doc_new_status = opts['doc_names'], opts.get('new_status', new_status)  # if no status is passed
        except TypeError:  # If opts is a list. We use default new_status from param
            doc_names, doc_new_status = opts, new_status

        for name in doc_names:                    # Iterate all over docs to update
            doc = frappe.get_doc(doctype, name)   # Getting Doc from current Doctype

            if doc.change_status(doc_new_status):  # If status can be changed. Prevent unnecessary updates
                updated_docs += 1                  # Count, because this document could be updated
                doc.flags.ignore_validate = True   # Set flag ON because Doc will be saved from bulk edit. No validations
                doc.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

            iter_doc += 1  # Count each time we iter a doc to change. We dont reset so we can count all doctypes.
            frappe.publish_progress(
                percent=(iter_doc * 100 / total_doc_names), title=msg_title,  # doctype=doctype, docname=name,
                description='Updating Status to {doctype}: {doc_name}'.format(doctype=doctype, doc_name=name),
            )

        # Creating Message to show with results of status change to doctype
        message.append('{updated} out of {total} {doctype}s have been updated to {new_status}.'.format(
            updated=updated_docs, total=len(doc_names), doctype=doctype, new_status=doc_new_status
        ))

    frappe.flags.mute_emails = frappe.flags.in_import = False  # Core: Reset all notifications and emails.

    frappe.msgprint(msg=message, title=msg_title, as_list=True, indicator='green')  # Show message as dialog
