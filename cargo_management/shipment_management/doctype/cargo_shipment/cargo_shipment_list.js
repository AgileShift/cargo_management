frappe.listview_settings['Cargo Shipment'] = {
    add_fields: ['status'],
    filters: [['status', '!=', 'Finished']],

	// TODO: Migrate to Document States? Maybe when frappe core starts using it.
	get_indicator: (doc) => [__(doc.status), {
		'Awaiting Departure': 'yellow',
		'In Transit': 'purple',
		'Sorting': 'green',
		'Finished': 'darkgrey',
	}[doc.status], 'status,=,' + doc.status],

    formatters: {
        transportation: (value) => cargo_management.transportation_formatter(value)
    }
}
