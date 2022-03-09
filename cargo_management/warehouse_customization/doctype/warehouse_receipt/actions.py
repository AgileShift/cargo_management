import frappe
from cargo_management.package_management.doctype.package.actions import find_carrier_by_tracking_number
# from cargo_management.utils import get_list_from_child_table, update_status_in_bulk
# from frappe import _


@frappe.whitelist(methods='GET')
def find_package_by_tracking_number(tracking_number: str):
    """ Tries to Find a Package Doc giving only a tracking number """
    result = find_carrier_by_tracking_number(tracking_number)

    # print('Result: {}'.format(result))

    coincidences = frappe.get_list('Package',
        fields=['name', 'tracking_number', 'customer_name', 'transportation_type'],
        or_filters={
            'name': ['LIKE', '%{}%'.format(result['search_term'])],
            'tracking_number': ['LIKE', '%{}%'.format(result['search_term'])]
        }
    )

    # TODO: Delete
    # print('Tracking Scanned: ' + tracking_number)
    # print('Search Term:      ' + result['search_term'])
    # print('Coincidences:     {}'.format(coincidences))

    if not coincidences:
        return False  # No Package with similar name or tracking_number
    elif len(coincidences) == 1 and tracking_number in (coincidences[0].name, coincidences[0].tracking_number):
        return coincidences[0]  # Only one coincidence and its equal. Exact match

    # TODO: what if only 1 coincidence and its a partial match. Its likely to be a exact match
    # TODO: What if multiple coincidences are find and 1 of them its a exact match?
    # TODO: if search request its inside consolidated

    return {'coincidences': coincidences, 'search_term': result['search_term']}


# TODO: Delete. this is unused.
# @frappe.whitelist(methods='POST')
# def update_status(source_doc_name: str, new_status: str):
#     It is more safe to get the doc from db that receive it from client-side as param
    # doc = frappe.get_cached_doc('Warehouse Receipt', source_doc_name)  # Getting the Warehouse Receipt Doc from db
    #
    # update_status_in_bulk(docs_to_update={
    #     'Package': get_list_from_child_table(doc.warehouse_receipt_lines, 'package')
    # }, new_status=new_status, msg_title=_('Confirm Packages'), mute_emails=doc.mute_emails)
