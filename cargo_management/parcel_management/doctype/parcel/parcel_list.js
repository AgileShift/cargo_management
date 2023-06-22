frappe.listview_settings['Parcel'] = {
	add_fields: ['status', 'carrier'],
	filters: [['status', 'not in', ['Finished', 'Cancelled', 'Never Arrived', 'Returned to Sender']]],

	onload(listview) {
		const {name: name_field, tracking_number: tracking_number_field, customer_name: customer_name_field} = listview.page.fields_dict;

		// The 'tracking_number' field is set because is the title field of the Doctype. So we remove from the 'standard_filters'
		tracking_number_field.wrapper.remove();

		// Set 'name' field tooltip and placeholder to match 'tracking_number' field
		name_field.wrapper.setAttribute('data-original-title', tracking_number_field.df.label);
		name_field.input.setAttribute('placeholder', tracking_number_field.df.placeholder);

		// Override: onchange() method set in frappe/list/base_list.js -> make_standard_filters()
		name_field.df.onchange = customer_name_field.df.onchange = function () {
			// Remove '%' added in frappe/list/base_list.js -> get_standard_filters() when the listview loads and update both UI and internal values
			this.value = this.input.value = this.get_input_value().replaceAll('%', '').trim().toUpperCase(); // this.set_input() is not working

			if (this.value !== this.last_value) {
				listview.filter_area.refresh_list_view(); // refresh_list_view() if the value has changed
			}
		};

		/* Override to add 'or_filters'. FIXME: Will be better to have it on backend to solve: gets_args + get_count_str + get_stats
		 * frappe hook: 'permission_query_conditions' Wont work, It get called after we have build the frappe
		 * check this: override_whitelisted_methods. The problem is this method is HEAVILY used
		 * TODO: listview.get_count_str() => This call frappe.db.count() using 'filters' not 'or_filters'
		 * TODO: listview.list_sidebar.get_stats() => This call frappe.desk.reportview.get_sidebar_stats using 'filters' not 'or_filters' */
		listview.get_args = function () {
			let args = frappe.views.ListView.prototype.get_args.call(listview);  // Calling his super for the args

			const name_filter = args.filters.findIndex(f => f[1] === 'name');  // f -> ['Doctype', 'field', 'sql_search_term', 'value']

			if (name_filter >= 0) {  // We have 'name' filter being filtered. -> name_filter will contain index if found
				args.filters.splice(name_filter, 1);  // Removing 'name' filter from 'filters'. It's a 'standard_filter'

				const search_term = cargo_management.find_carrier_by_tracking_number(name_field.get_input_value()).search_term;

				args.or_filters = ['name', 'tracking_number', 'consolidated_tracking_numbers'].map(field => [
					args.doctype, field, 'like', '%' + search_term + '%'
				]); // Mapping each field to 'or_filters' for the necessary fields to search
			}

			return args;
		};

		// Override to add a dropdown. If the 'show' function within the 'button' property is null or returns False it won't create the 'settings_button'
		listview.get_meta_html = function (doc) {
			let $html = $(frappe.views.ListView.prototype.get_meta_html.call(listview, doc)); // Calling his super for the html string value

			const urls_html = cargo_management.load_carrier_settings(doc.carrier).urls.reduce((acc, url) => {
				return acc + `<a class="dropdown-item" href="${url.url + doc.tracking_number}" target="_blank">${url.title}</a>`;
			}, ''); // Loading the Carrier URLs then return a single string of items for the dropdown

			// Find the parent element of 'settings_button' and 'assigned_to', then replace with our custom 'button'. Check the core function on list_view.js
			$html.find('.hidden-md.hidden-xs').html(`
				<div class="list-actions dropdown">
					<a class="btn btn-default btn-xs dropdown-toggle" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">${__('Carriers')}</a>
					<div class="dropdown-menu dropdown-menu-right">${urls_html}</div>
				</div>
			`);

			return $html.prop('outerHTML');
		};
    },

	// Unused: Light Blue. // TODO: Migrate to Document States? Maybe when frappe core starts using it.
	get_indicator: (doc) => [__(doc.status), {
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
	}[doc.status], 'status,=,' + doc.status],

	formatters: {
		transportation: (value) => cargo_management.transportation_formatter(value),
		name: (value, df, doc) => (value !== doc.tracking_number) ? `<b>${value}</b>` : ''
	}
};
