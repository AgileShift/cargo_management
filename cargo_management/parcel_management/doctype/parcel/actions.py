import frappe


@frappe.whitelist(methods='POST')
def get_data_from_api(source_name: str):
    """ Returns the Parcel Doc with new data from API if it was possible to fetch. """
    return frappe.get_cached_doc('Parcel', source_name).save(request_data_from_api=True)
