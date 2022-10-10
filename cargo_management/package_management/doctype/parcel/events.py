import frappe


def check_parcel_delivery():
    pass
    #carriers = frappe.get_file_json(frappe.get_app_path('Cargo Management', 'public', 'carriers.json'))['CARRIERS']

    #parcel = frappe.get_doc('Parcel', 'TESTING')

    #parcel.consolidated_tracking_numbers = frappe.utils.random_string(20)

    #parcel.flags.ignore_permissions = True
    #parcel.flags.ignore_mandatory = True
    #parcel.save()
