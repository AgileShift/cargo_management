import frappe


@frappe.whitelist(methods='POST')  # Because this action is set from Doctype Actions, we can't control this.
def update_data_from_carrier(doc):
    """ Used as Action button in Doctype: Fetch new data from API if we can track then update the doc if its open """
    doc = frappe.parse_json(doc)
    package = frappe.get_cached_doc('Package', doc.get('name'))

    # Verify if we can track, because .save() will update doc, even if we can't track. Then an extra query has been done
    if package.can_track():
        # Trigger before_save() who check for the flag that avoid validation checks
        return package.save(requested_to_track=True, ignore_permissions=True)


@frappe.whitelist(methods='GET')
def get_carrier_detail_page_url(carrier: str):
    """ Util: Return the carrier detail page URL to append to a tracking number. Used in a Form Action Button """
    return \
        frappe.get_cached_value('Package Carrier', carrier, 'carrier_detail_page_url') or \
        frappe.db.get_single_value('Package Settings', 'default_carrier_detail_page_url', cache=True)


@frappe.whitelist(methods='GET')
def get_explained_status(source_name: str):
    """ Util: Return explained status message from doc object """
    return frappe.get_cached_doc('Package', source_name).get_explained_status()


@frappe.whitelist(methods='GET')
def find_carrier_from_tracking_number(tracking_number: str):


    if '1Z' in tracking_number:
        return 'UPS Tracking'
    elif 'TBA' in tracking_number:
        return 'Amazon Tracking'
    elif 'JJD' in tracking_number:
        frappe.throw('Convert to DHL Tracking')
    elif any(s in tracking_number for s in ['LY', 'LB']):
        return 'Possibly a USPS Tracking'

    return 'HELLOW'
