frappe.listview_settings['Cargo Shipment Receipt'] = {
    add_fields: ['status'],
    filters: [
        ['status', '!=', 'Finished'],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        const status_color = {
            'Awaiting Receipt': 'lightblue',
            'Sorting': 'orange',
            'Finished': 'green'
        };

        return [__(doc.status), status_color[doc.status], 'status,=,' + doc.status];
    }
}