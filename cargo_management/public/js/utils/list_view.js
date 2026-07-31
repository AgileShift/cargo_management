const cargo_management = frappe.provide('cargo_management');

cargo_management.list_view = {
	get_indicator: (status) => [__(status), {
		'Open': 'light-blue',

		'Awaiting Receipt': 'blue',
		'Awaiting Confirmation': 'orange',
		'In Extraordinary Confirmation': 'pink',
		'Awaiting Departure': 'yellow',
		'In Transit': 'purple',
		'In Customs': 'gray',
		'Sorting': 'green',
		'To Bill': 'green',
		'Unpaid': 'red',
		'For Delivery or Pickup': 'cyan',
		'Finished': 'darkgrey',
		'Cancelled': 'red',
		'Never Arrived': 'red',
		'Returned to Sender': 'red',
	}[status], 'status,=,' + status],

	transportation_formatter(transportation) {
		if (!transportation) return '';

		const opts = cargo_management.TRANSPORTATIONS[transportation] || {color: 'gray'};
		const icon = opts.icon ? cargo_management.icon_html(opts.icon) : '';

		return `<span class="indicator-pill ${opts.color} filterable no-indicator-dot ellipsis" data-filter="transportation,=,${transportation}">
			<span class="ellipsis">${__(transportation)}${icon}</span>
		</span>`; // See more of this on list/list_view.js -> get_indicator_html();
	}
};
