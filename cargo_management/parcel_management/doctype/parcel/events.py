import frappe


def get_permission_query_conditions(user):
	# Problem is permission_query_conditions is called after the get() method
	# and the get_methods calls the frappe.form_dict, so its too late to change it!
	print('get_permission_query_conditions: PARCEL')

	print(frappe.form_dict.cmd)
	if frappe.form_dict.cmd not in ('frappe.desk.reportview.get', 'frappe.desk.reportview.get_count', 'frappe.desk.reportview.get_sidebar_stats'):
		return ''

	filters = frappe.parse_json(frappe.form.filters)
	print('Filters:', frappe.form.filters)

	tracking_number_filter = ''
	for f in filters:
		if f[1] == 'tracking_number':
			tracking_number_filter = f[3]

			frappe.form.or_filters = []

			for or_f in ['name', 'tracking_number']:
				frappe.form.or_filters.append([frappe.form.doctype, or_f, 'like', f[3]])
			filters.remove(f)

			frappe.form.filters = filters
			break

		print('Looping: ', f)

	frappe.form_dict = frappe.form

	return ''

	return f"""(`tabParcel`.name like '%92%')"""


@frappe.whitelist()
def get_parcel_query(doctype, txt, searchfield, start, page_len, filters):
	print('get_parcel_query: PARCEL')

	return frappe.db.sql(
		""" SELECT name, tracking_number
		FROM `tabParcel`
			WHERE tracking_number LIKE %(txt)s
		LIMIT %(page_len)s OFFSET %(start)s
		""",
		dict(start=start, page_len=page_len, txt=txt),
	)
