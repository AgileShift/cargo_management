frappe.listview_settings['Cargo Shipment'] = {
	filters: [['status', '!=', 'Finished']],

	get_indicator: (doc) => cargo_management.list_view.get_indicator(doc.status),

	formatters: {
		transportation: (value) => cargo_management.list_view.transportation_formatter(value)
	}
};
