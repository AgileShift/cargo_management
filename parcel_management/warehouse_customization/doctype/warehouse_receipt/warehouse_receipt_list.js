frappe.listview_settings['Warehouse Receipt'] = {
    add_fields: ['status'],
    filters: [
        ['status', '!=', 'Closed'],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        const status_color = {
            'Open': 'yellow',
            'In Transit': 'purple',
            'Closed': 'green',
        };

        return [__(doc.status), status_color[doc.status], 'status,=,' + doc.status];
    }
}