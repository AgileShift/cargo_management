import frappe


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
