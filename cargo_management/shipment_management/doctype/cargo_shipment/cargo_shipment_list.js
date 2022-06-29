frappe.listview_settings['Cargo Shipment'] = {
    //add_fields: ['status'],  // TODO: Improve here. because we have extra data!. also what this is for?
    filters: [
        ['status', '!=', 'Finished'],
    ],
    hide_name_column: true,

    get_indicator: function (doc) {
        const status_color = {
            'Awaiting Departure': 'yellow',
            'In Transit': 'purple',
            'Sorting': 'orange',
            'Finished': 'green',
        };

        return [__(doc.status), status_color[doc.status], 'status,=,' + doc.status];
    },

    formatters: {
        transportation: (value) => cargo_management.transportation_formatter(value)
    }
}