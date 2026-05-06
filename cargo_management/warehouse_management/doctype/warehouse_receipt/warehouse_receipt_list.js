frappe.listview_settings['Warehouse Receipt'] = {
	filters: [['status', 'not in', ['Sorting', 'Finished']]],

	get_indicator: (doc) => cargo_management.get_indicator(doc.status),

	formatters: {
		transportation: (value) => cargo_management.transportation_formatter(value)
	}
}
