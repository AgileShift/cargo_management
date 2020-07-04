import json
import webbrowser

import frappe


@frappe.whitelist(allow_guest=False)
def update_data_from_carrier(doc):
    """ Fetch new data from carrier if we can track and update the doc if its open. """
    doc = json.loads(doc)
    parcel = frappe.get_doc('Parcel', doc.get('name'))

    # Verify if we can track, because .save() will update doc, even if we can't track. Then we would have to reload doc.
    if parcel.can_track():
        parcel.flags.ignore_track_validation = True  # Setting bypass flag On. See Parcel Doctype flags
        parcel.save()  # Trigger before_save who calls can_track with the bypass flag on so we avoid revalidation check
        frappe.publish_realtime('new_carrier_data', user=frappe.session.user)  # Send update to frontend to reload.


@frappe.whitelist(allow_guest=False)
def visit_carrier_detail_page(doc):
    """ Opens a browser tab to the carrier detail page with all the package information from carrier."""
    doc = json.loads(doc)  # Package object

    carrier_detail_page_url = frappe.get_value('Parcel Carrier', doc.get('carrier'), 'carrier_detail_page_url')

    if not carrier_detail_page_url:  # The carrier doesnt have a specific detail page. we must use the default
        carrier_detail_page_url = frappe.get_value('Parcel Settings', None, 'default_carrier_detail_page_url')

    webbrowser.open_new_tab(carrier_detail_page_url + doc.get('tracking_number'))
