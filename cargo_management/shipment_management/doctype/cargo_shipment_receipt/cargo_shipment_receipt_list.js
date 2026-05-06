frappe.listview_settings['Cargo Shipment Receipt'] = {
	filters: [['status', '!=', 'Finished']],

	get_indicator: (doc) => cargo_management.get_indicator(doc.status),

	formatters: {
		transportation: (value) => cargo_management.transportation_formatter(value)
	}
}
