import frappe


def get_list_from_child_table(child_lines: list, field: str):
    """ This takes a List of Dicts [{}] and return a List of Uniques values. """
    return list(set(child_line.get(field) for child_line in child_lines if child_line.get(field) is not None))  # FIXME: Performance?


def update_status_in_bulk(docs_to_update: dict, new_status: str = None, msg_title: str = '', mute_emails: bool = True):
    """
    This tries to update all docs statuses, no matter what doctype is.

    @param docs_to_update: {'Doctype': [names] } or { 'Doctype': {'doc_names': [names], 'new_status': 'string' } }
    @param new_status: str. To be used in doctypes where new status was not explicitly declared in docs_to_update dict
    @param msg_title: str. Title for the dialog
    @param mute_emails: bool. This activate or deactivates notifications on backend. True if not sent
    """
    message, iter_doc = [], 0  # For Gathering Message, counter of current iter of all doc_names
    total_doc_names = sum(len(docs) if type(docs) is list else len(docs['doc_names']) for docs in docs_to_update.values())

    frappe.flags.mute_emails = frappe.flags.in_import = mute_emails  # Core: Silence all notifications and emails.

    for doctype, opts in docs_to_update.items():  # Iterate all over Doctypes. opts can be: Dict or List.
        updated_docs = 0                          # Reset Updated Docs Counter to zero each time we change of Doctype.

        try:  # if opts is a Dict -> {'doc_names': [doc_names], 'new_status': 'string' }
            doc_names, doc_new_status = opts['doc_names'], opts.get('new_status', new_status)  # if no status is passed
        except TypeError:  # if opts is a List. We use default new_status from def params
            doc_names, doc_new_status = opts, new_status

        for name in doc_names:                    # Iterate all over docs to update
            doc = frappe.get_doc(doctype, name)   # Getting Doc from current DocType

            if doc.change_status(doc_new_status):  # If status can be changed. Prevent unnecessary updates
                updated_docs += 1                  # Count, because this document could be updated
                doc.flags.ignore_validate = True   # Set flag ON because Doc will be saved from bulk edit. No validations
                doc.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

            iter_doc += 1  # Count each time we iter a doc to change. We don't reset soo we can count all DocTypes.
            frappe.publish_progress(  # TODO: Sometimes this dont get to 100%
                percent=(iter_doc / total_doc_names * 100), title=msg_title,  # doctype=doctype, docname=name,
                description='Updating Status to {doctype}: {doc_name}'.format(doctype=doctype, doc_name=name)
            )

        # Creating Message to show with results of status change to doctype
        message.append('{updated} out of {total} {doctype}s have been updated to {new_status}.'.format(
            updated=updated_docs, total=len(doc_names), doctype=doctype, new_status=doc_new_status
        ))

    frappe.flags.mute_emails = frappe.flags.in_import = False  # Core: Reset all notifications and emails.

    frappe.msgprint(msg=message, title=msg_title, as_list=True, indicator='green')  # Show message as dialog


def find_carrier_from_tracking_number(tracking_number: str):
    """ Find the carrier of a Package """
    # TODO: Sync the "Carrier Code" with the Doctype "Package Carrier" in case we have multiple API Provider
    print(tracking_number)
    print('Estoy por aca xD')

    if '1Z' in tracking_number:
        return 'USPS'

    return 'HELLOW'

    # return tracking_number
