import frappe


@frappe.whitelist()
def update_data_from_carrier(doc):
    """ Used as Action button in Doctype: Fetch new data from carrier if we can track and update the doc if its open """
    doc = frappe.parse_json(doc)
    package = frappe.get_doc('Package', doc.get('name'))

    # Verify if we can track, because .save() will update doc, even if we can't track. Then we would have to reload doc.
    if package.can_track():
        package.flags.requested_to_track = True  # Set bypass flag ON. See Package Doctype flags. Go directly to track.
        package.save()  # Trigger before_save() who checks for the bypass flag. We avoid revalidation checks.

    return {}  # FIX: To prevent reload_doc being called twice by: execute_action() called if using "Server Action"


@frappe.whitelist()
def update_data_from_carrier_bulk(names):
    # TODO: FINISH
    names = frappe.parse_json(names)

    # for name in names:
    #     update_data_from_carrier({
    #         'name': name
    #     })


@frappe.whitelist()
@frappe.read_only()
def get_carrier_detail_page_url(carrier: str):
    """ Util: Return the carrier detail page URL to append to a tracking number. Used in a Form Action Button """
    return \
        frappe.get_value('Package Carrier', carrier, 'carrier_detail_page_url', cache=True) or \
        frappe.db.get_single_value('Package Settings', 'default_carrier_detail_page_url', cache=True) # TODO: get_cached_doc?


@frappe.whitelist()
@frappe.read_only()
def get_explained_status(source_name: str):
    """ Util: Return explained status message from doc object """
    return frappe.get_doc('Package', source_name, cache=True).get_explained_status()  # TODO: get_cached_doc?
