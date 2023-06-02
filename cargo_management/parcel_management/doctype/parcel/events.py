import frappe


def check_parcel_delivery():
	# carriers = frappe.get_file_json(frappe.get_app_path('Cargo Management', 'public', 'carriers.json'))['CARRIERS']

	# parcel = frappe.get_doc('Parcel', 'TESTING')

	# parcel.consolidated_tracking_numbers = frappe.utils.random_string(20)

	# parcel.flags.ignore_permissions = True
	# parcel.flags.ignore_mandatory = True
	# parcel.save()
	pass


def get_permission_query_conditions(user):
	# Problem is permission_query_conditions is called after the get() method
	# and the get_methods calls the frappe.form_dict, so its too late to change it!

	print(frappe.form_dict.cmd)
	if frappe.form_dict.cmd not in ('frappe.desk.reportview.get', 'frappe.desk.reportview.get_count', 'frappe.desk.reportview.get_sidebar_stats'):
		return ''

	filters = frappe.parse_json(frappe.form.filters)
	print("get_permission_query_conditions: ", filters)

	for f in filters:
		if f[1] == 'name':
			frappe.form.or_filters = []
			for or_f in ['name', 'tracking_number', 'consolidated_tracking_numbers']:
				frappe.form.or_filters.append([frappe.form.doctype, or_f, 'like', f[3]])
			filters.remove(f)
			frappe.form.filters = filters
			break
		print('Looping: ', f)

	frappe.form_dict = frappe.form

	return ''
