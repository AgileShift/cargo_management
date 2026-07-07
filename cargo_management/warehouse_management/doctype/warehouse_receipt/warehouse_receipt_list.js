frappe.listview_settings['Warehouse Receipt'] = {
	filters: [['status', 'not in', ['Sorting', 'Finished']]],

	get_indicator: (doc) => cargo_management.list_view.get_indicator(doc.status),

	formatters: {
		transportation: (value) => cargo_management.list_view.transportation_formatter(value)
	}
};
