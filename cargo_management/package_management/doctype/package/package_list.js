frappe.listview_settings['Package'] = {
    add_fields: ['status', 'carrier'], // TODO: Improve here. because we have extra data!. also what this is for?
    filters: [
        ['status', 'not in', ['Finished', 'Cancelled', 'Returned to Sender']],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        const status_color = {
            'Awaiting Receipt': 'lightblue',
            'Awaiting Confirmation': 'orange',
            'In Extraordinary Confirmation': 'pink',
            'Awaiting Departure': 'cyan',
            'In Transit': 'purple',
            'In Customs': 'gray',
            'Sorting': 'yellow',
            'To Bill': 'orange',
            'Unpaid': 'red',
            'To Deliver or Pickup': 'blue',
            'Finished': 'green',
            'Cancelled': 'darkgrey',
            'Never Arrived': 'red',
            'Returned to Sender': 'red',
        };

        return [__(doc.status), status_color[doc.status], 'status,=,' + doc.status];
    },

    formatters: {
        transportation_type(val) {
            let color = (val === 'Sea') ? 'blue' : 'red';
            return `<span class="indicator-pill ${color} filterable ellipsis"
                data-filter="transportation_type,=,${frappe.utils.escape_html(val)}">
				<span class="ellipsis"> ${val} </span>
			<span>`;
        }
    },
    button: {
        show(doc) {
            return doc.name;
        },
        get_label() {
            return __('Carrier page')
        },
        get_description() {
            return __('Open carrier page')
        },
        action(doc) {
            frappe.call({
                method: 'cargo_management.package_management.doctype.package.actions.get_carrier_tracking_url',
                type: 'GET',
                args: {carrier: doc.carrier},
                freeze: true,
                freeze_message: __('Opening carrier detail page...'),
                callback: (r) => window.open(r.message + doc.tracking_number, '_blank')
            });
        },
    },

    onload: function (listview) {
        listview.get_args = function () {  // Override only instance method
            let args = frappe.views.ListView.prototype.get_args.call(listview);  // Calling his super

            args.filters.some((filter, i) => {
                if (filter[1] === 'name') {  // If we find name move it from filters to or_filters and expand it
                    return args.or_filters = [
                        args.filters.splice(i, 1)[0],  // Remove and add ;)
                        [filter[0], 'tracking_number', filter[2], filter[3]],
                        [filter[0], 'consolidated_tracking_numbers', filter[2], filter[3]],
                    ];
                }
            });

            return args;
        }

        // listview.page.add_actions_menu_item(__('Update data from carrier'), function () {
            // TODO FINISH.... This is work in progress
            // Bulk Dialog - should sent email if status is changed?
            // Bulk show_progress. This actually reloads the form? if so. how many times?
            // listview.call_for_selected_items(
            //     'cargo_management.package_management.doctype.package.actions.update_data_from_carrier_bulk'
            //  );
        // })
    }
}
