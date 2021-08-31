frappe.listview_settings['Warehouse Receipt'] = {
    add_fields: ['status'],
    filters: [
        ['status', '!=', 'Finished'],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        const status_color = {
            'Awaiting Departure': 'yellow',
            'In Transit': 'purple',
            'Sorting': 'orange',
            'Finished': 'green',
        };

        return [__(doc.status), status_color[doc.status], 'status,=,' + doc.status];
    }
}