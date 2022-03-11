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
def get_carrier_tracking_url(carrier: str):
    """ Util: Return the carrier tracking URL. Used in a Form Action Button """
    return \
        frappe.get_cached_value('Package Carrier', carrier, 'carrier_detail_page_url') or \
        frappe.db.get_single_value('Package Settings', 'default_carrier_detail_page_url', cache=True)


@frappe.whitelist(methods='GET')
def get_explained_status(source_name: str):
    """ Util: Return explained status message from Package """
    return frappe.get_cached_doc('Package', source_name).get_explained_status()


@frappe.whitelist(methods='GET')
def find_carrier_by_tracking_number(tracking_number: str):
    """ Find a carrier if a tracking number is passed.

    - https://pages.message.fedex.com/barcodescan_home/

    # TODO: Add More Carriers
    # TODO: Python 3.10: Migrate to switch case or Improve performance?
    # FIXME: if only TBA, 1Z, 1LS is sent it should fail
    # FIXME: Run if tracking_number length is more than 6?
    """
    tracking_number = tracking_number.strip().upper()  # Sanitize field

    if not tracking_number:
        return {}

    tracking_number_len = len(tracking_number)
    carrier, search_term = 'Unknown', tracking_number  # TODO: search_term = 2/4 and 3/4 of the tracking. At bottom

    if 'TBA' in tracking_number:
        carrier = 'Amazon'
    elif '1Z' in tracking_number:
        carrier = 'UPS'
    elif '1LS' in tracking_number:
        carrier = 'LaserShip'
    elif tracking_number_len == 10:
        carrier = 'DHL'

    # TODO elif any(s in tracking_number for s in ['LY', 'LB']):
    #     return 'Possibly a USPS Tracking'

    # FedEx or USPS. Matches starting with zipcode(420xxxxx) or with 92612. To search we will return starting with 612
    elif tracking_number_len == 22 and tracking_number[:5] == '92612':
        carrier, search_term = '', tracking_number[2:]      # *92612*90980949456651012. Or *926129*
    elif tracking_number_len == 30 and tracking_number[8:13] == '92612':
        carrier, search_term = '', tracking_number[10:]     # 42033166*92612*90980949456651012. Or *926129*

    elif tracking_number_len in [22, 26] and tracking_number[0] == '9':
        carrier = 'USPS'                                    # *9*400111108296364807659
    elif tracking_number_len in [30, 34] and tracking_number[8] == '9':
        carrier, search_term = 'USPS', tracking_number[8:]  # 42033165*9*274890983426386918697. First 8 digits: 420xxxxx(zipcode)

    elif tracking_number_len == 12:
        carrier = 'FedEx',
    elif tracking_number_len == 20 and tracking_number[:3] == '612':
        carrier = 'FedEx',                                    # *612*90982157320543198. Or *6129*
    elif tracking_number_len == 34 and tracking_number[22] != 0:
        carrier, search_term = 'FedEx', tracking_number[22:]  # 9622001900005105596800*5*49425980480. Last 12 digits is tracking

    elif 'JD' in tracking_number:  # or JJD
        frappe.throw('Convert to DHL Tracking')  # FIXME: Maybe we can convert it?

    return {'carrier': carrier, 'search_term': search_term, 'tracking_number': tracking_number}
