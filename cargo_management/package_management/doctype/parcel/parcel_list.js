frappe.listview_settings['Parcel'] = {
    add_fields: ['carrier'],
    filters: [['status', 'not in', ['Finished', 'Cancelled', 'Never Arrived', 'Returned to Sender']]],
    hide_name_column: false,

    onload: function (listview) {
        const {name: name_field, tracking_number: tracking_number_fields, customer_name: customer_name_field} = listview.page.fields_dict;

        // Remove tracking_number field from Standard Filter(Is set because field is the Title of the Doctype)
        tracking_number_fields.$wrapper.remove();

        // Update placeholder and help-text
        name_field.$wrapper.attr('data-original-title', __('Tracking numbers'));
        name_field.$input.attr('placeholder', __('Tracking numbers'));

        // FIXME: Issue in v14: https://github.com/frappe/frappe/issues/17183 -> last_value same as value
        // Override: name_field & customer_name_field -> df.onchange() method set in make_standard_filters(). Call refresh_list_view() if value has changed

        // TODO: listview.get_count_str() => This call frappe.db.count() using 'filters' not 'or_filters'
        // TODO: listview.list_sidebar.get_stats() => This call frappe.desk.reportview.get_sidebar_stats using 'filters' not 'or_filters'
        // Override: Use the 'search_term' of the 'name' field in the 'or_filters', remove '%' added in get_standard_filters()
        listview.get_args = () => {
            // Removing '%' added when the listview loads first time. Also sanitize field and change UI
            name_field.value = name_field.input.value = name_field.get_input_value().replaceAll('%', '').trim().toUpperCase();
            customer_name_field.input.value = customer_name_field.get_input_value().replaceAll('%', '').trim().toUpperCase();

            let args = frappe.views.ListView.prototype.get_args.call(listview);  // Calling his super for the args

            const name_filter = args.filters.findIndex(f => f[1] === 'name');  // f -> ['Doctype', 'field', 'sql_search_term', 'value']

            if (name_filter >= 0) {  // We have 'name' filter being filtered. -> Will return index if found
                args.filters.splice(name_filter, 1);  // Removing 'name' filter from 'filters'. It's a 'standard_filter'

                const data = cargo_management.find_carrier_by_tracking_number(name_field.get_input_value());

                args.or_filters = [
                    ['Parcel', 'name', 'like', '%' + data.search_term + '%'],
                    ['Parcel', 'tracking_number', 'like', '%' + data.search_term + '%'],
                    ['Parcel', 'consolidated_tracking_numbers', 'like', '%' + data.search_term + '%']
                ];
            }

            return args;
        }
    },

    get_indicator: function (doc) {
        //Unused: Light Blue
        const status_color = {
            'Awaiting Receipt': 'blue',
            'Awaiting Confirmation': 'orange',
            'In Extraordinary Confirmation': 'pink',
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
            // TODO: Make this a List of buttons
            cargo_management.load_carrier_settings(doc.carrier)
                .then(settings => window.open(settings.urls[0].url + doc.tracking_number, '_blank'));
        },
    },

    formatters: {
        transportation: (value) => cargo_management.transportation_formatter(value),
        name: (value, df, doc) => (value !== doc.tracking_number) ? value.bold() : ''
    }
};
