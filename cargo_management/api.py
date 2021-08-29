import frappe

from cargo_management.package_management.doctype.package.actions import get_carrier_detail_page_url


@frappe.whitelist(allow_guest=True)
@frappe.read_only()
def get_package_for_customer_query(tracking_number: str):
    """ Returns the package details if was able to find it! """

    # TODO: Making a Special Search def: for eg. USPS or changed tracking number.
    package = frappe.get_cached_doc('Package', tracking_number)

    # Construct Carrier Detail Page URL
    carrier_detail_page = get_carrier_detail_page_url(package.carrier) + package.tracking_number

    return {
        'name': package.name,
        'tracking_number': package.tracking_number,
        'carrier': package.carrier,
        'status': package.status,
        'carrier_status': package.carrier_status,
        'carrier_status_detail': package.carrier_status_detail,
        'carrier_last_detail': package.carrier_last_detail,
        'carrier_est_delivery': package.carrier_est_delivery,
        'carrier_est_weight': package.carrier_est_weight,
        'message': package.get_explained_status(),  # TODO: Best way to do it?
        'carrier_detail_page': carrier_detail_page
    }
