frappe.listview_settings['Cargo Shipment Receipt'] = {
    add_fields: ['status'],
    hide_name_column: true,

    get_indicator(doc) {
        const status_color = {
            // TODO: Finish -> add In Sorting or Sorting?
            'Open': 'yellow',
            'Closed': 'green'
        };

        return [__(doc.status), status_color[doc.status], 'status,=,' + doc.status];
    }
}