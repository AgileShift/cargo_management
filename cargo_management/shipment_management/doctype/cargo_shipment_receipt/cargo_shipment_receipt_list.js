frappe.listview_settings['Cargo Shipment Receipt'] = {
	filters: [['status', '!=', 'Finished']],

	// TODO: Migrate to Document States? Maybe when frappe core starts using it.
	get_indicator: (doc) => [__(doc.status), {
		'Awaiting Receipt': 'blue',
		'Sorting': 'orange',
		'Finished': 'green'
	}[doc.status], 'status,=,' + doc.status],

}
