frappe.listview_settings['Package'] = {
    //add_fields: ['status', 'carrier'], // TODO: Improve here. because we have extra data!. also what this is for?
    filters: [
        ['status', 'not in', ['Finished', 'Cancelled', 'Never Arrived', 'Returned to Sender']],
    ],
    hide_name_column: true,

    onload: function (listview) {
        const name_field = listview.page.fields_dict['name'];

        // Update placeholder and help-text
        name_field.$wrapper.attr('data-original-title', __('Tracking Numbers'));
        name_field.$input.attr('placeholder', __('Tracking Numbers'));

        // TODO: listview.get_count_str() => This call frappe.db.count() using 'filters' not 'or_filters'
        // TODO: listview.list_sidebar.get_stats() => This call frappe.desk.reportview.get_sidebar_stats using 'filters' not 'or_filters'
        listview.get_args = () => {  // Override only instance method
            let args = frappe.views.ListView.prototype.get_args.call(listview);  // Calling his super for the args

            const name_filter = args.filters.findIndex(f => f[1] === 'name');  // f -> ['Doctype', 'field', 'sql_search_term', 'value']

            if (name_filter >= 0) {  // We have 'name' filter being filtered. -> Will return index if found
                args.filters.splice(name_filter, 1);  // Removing 'name' filter from 'filters'. It's a 'standard_filter'

                // Removing '%' added when the listview loads first time & trim spaces when values are pasted
                name_field.input.value = name_field.get_value().replaceAll('%', '').trim().toUpperCase(); // Makes the UI change

                const data = cargo_management.find_carrier_by_tracking_number(name_field.get_value());

                args.or_filters = [
                    ['Package', 'name', 'like', '%' + data.search_term + '%'],
                    ['Package', 'tracking_number', 'like', '%' + data.search_term + '%'],
                    ['Package', 'consolidated_tracking_numbers', 'like', '%' + data.search_term + '%'],
                ];
            }

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
    },

    get_indicator: function (doc) {
        const status_color = {
            'In Extraordinary Confirmation': 'pink',

            // cyan
            // TODO: Range of colors
            'Awaiting Receipt': 'blue',
            'Awaiting Confirmation': 'orange',
            'Awaiting Departure': 'yellow',
            'In Transit': 'purple',
            'In Customs': 'gray',
            'Sorting': 'green',
            'To Bill': 'green',
            'Unpaid': 'red',
            'To Deliver or Pickup': 'cyan',
            'Finished': 'darkgrey',

            'Cancelled': 'red',
            'Never Arrived': 'red',
            'Returned to Sender': 'red',
        };

        return [__(doc.status), status_color[doc.status], 'status,=,' + doc.status];
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

    formatters: {
        transportation: (value) => cargo_management.transportation_formatter(value)
    }
};
