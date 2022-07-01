frappe.listview_settings['Package'] = {
    //add_fields: ['status', 'carrier'], // TODO: Improve here. because we have extra data!. also what this is for?
    filters: [
        ['status', 'not in', ['Finished', 'Cancelled', 'Never Arrived', 'Returned to Sender']],
    ],
    hide_name_column: true,

    onload: function (listview) {
        const {name: name_field, customer_name: customer_name_field} = listview.page.fields_dict;

        // Update placeholder and help-text
        name_field.$wrapper.attr('data-original-title', __('Tracking Numbers'));
        name_field.$input.attr('placeholder', __('Tracking Numbers'));

        // Override: onchange() method set in make_standard_filters(). We call refresh_list_view() if value has changed
        name_field.df.onchange = customer_name_field.df.onchange = function () {
            this.value = this.input.value = this.get_input_value().trim().toUpperCase();  // Change UI and internal value

            if (this.value !== this.last_value)
                listview.filter_area.refresh_list_view(); // Same as make_standard_filters()
        };

        // TODO: listview.get_count_str() => This call frappe.db.count() using 'filters' not 'or_filters'
        // TODO: listview.list_sidebar.get_stats() => This call frappe.desk.reportview.get_sidebar_stats using 'filters' not 'or_filters'
        // Override: Use the 'search_term' of the 'name' field in the 'or_filters', remove '%' added in get_standard_filters()
        listview.get_args = () => {
            // Removing '%' added when the listview loads first time
            name_field.value = name_field.input.value = name_field.get_input_value().replaceAll('%', '');
            customer_name_field.input.value = customer_name_field.get_input_value().replaceAll('%', '');

            let args = frappe.views.ListView.prototype.get_args.call(listview);  // Calling his super for the args

            const name_filter = args.filters.findIndex(f => f[1] === 'name');  // f -> ['Doctype', 'field', 'sql_search_term', 'value']

            if (name_filter >= 0) {  // We have 'name' filter being filtered. -> Will return index if found
                args.filters.splice(name_filter, 1);  // Removing 'name' filter from 'filters'. It's a 'standard_filter'

                const data = cargo_management.find_carrier_by_tracking_number(name_field.get_input_value());

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
            // TODO: WORK ON THIS
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
