import frappe


@frappe.whitelist(allow_guest=False)
def update_data_from_carrier(doc):
    """ Used as Action button in Doctype: Fetch new data from carrier if we can track and update the doc if its open """
    doc = frappe.parse_json(doc)
    parcel = frappe.get_doc('Parcel', doc.get('name'))

    # Verify if we can track, because .save() will update doc, even if we can't track. Then we would have to reload doc.
    if parcel.can_track():
        parcel.flags.requested_to_track = True  # Set bypass flag ON. See Parcel Doctype flags. Go directly to track.
        parcel.save()  # Trigger before_save() who checks for the bypass flag. We avoid revalidation checks.


@frappe.whitelist(allow_guest=False)
def get_carrier_detail_page_url(carrier: str):
    """ Util: Return the carrier detail page URL to append to a tracking number. Used in a Form Action Button """
    return \
        frappe.get_value('Parcel Carrier', carrier, 'carrier_detail_page_url', cache=True) or \
        frappe.db.get_single_value('Parcel Settings', 'default_carrier_detail_page_url', cache=True)
