frappe.listview_settings['Warehouse Receipt'] = {
	filters: [['status', 'not in', ['Sorting', 'Finished']]],
	hide_name_column: true,

	onload(listview) {
		listview.page.sidebar.toggle(false); // Hide Sidebar
	},

	before_render() {},

	// TODO: Migrate to Document States? Maybe when frappe core starts using it.
	get_indicator: (doc) => [__(doc.status), {
		'Draft': 'gray',
		'Open': 'orange',
		'Awaiting Departure': 'yellow',
		'In Transit': 'purple',
		'Sorting': 'green',
		'Finished': 'darkgrey',
	}[doc.status], 'status,=,' + doc.status],

	formatters: {
		transportation(val) {
			let color = (val === 'Sea') ? 'blue' : 'red';
			return `<span class="indicator-pill ${color} filterable ellipsis"
                data-filter="transportation,=,${frappe.utils.escape_html(val)}">
				<span class="ellipsis"> ${val} </span>
			<span>`;
		}
	}
}
