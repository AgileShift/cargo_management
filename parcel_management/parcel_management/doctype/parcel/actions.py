import json

import frappe


@frappe.whitelist(allow_guest=False)
def update_data_from_carrier(doc):
    """ Fetch new data from carrier if we can track and update the doc if its open. """
    doc = json.loads(doc)
    parcel = frappe.get_doc('Parcel', doc.get('name'))

    # Verify if we can track, because .save() will update doc, even if we can't track. Then we would have to reload doc.
    if parcel.can_track():
        parcel._get_data_from_easypost_api()
        parcel.save()  # Trigger before_save who calls can_track with the bypass flag on so we avoid revalidation check
        frappe.publish_realtime('new_carrier_data', user=frappe.session.user)  # Send update to frontend to reload.

# Here must exists the: 'Visit carrier detail page' Button that lives in parcel.js -> Using webbrowser
