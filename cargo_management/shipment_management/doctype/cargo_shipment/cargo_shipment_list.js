frappe.listview_settings['Cargo Shipment'] = {
	filters: [['status', '!=', 'Finished']],

	onload(listview) {
		listview.page.sidebar.toggle(false); // Hide Sidebar to better focus on the doc
	},

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
