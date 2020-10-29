frappe.listview_settings['Shipment'] = {
    add_fields: ['status'],
    filters: [
        ['status', '!=', 'Received'],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        // TODO: Finish Indicator
        switch (doc.status) {
            case 'Open':
                return [__('Open'), 'yellow', 'status,=,Open']
            case 'In Transit':
                return [__('In Transit'), 'purple', 'status,=,In Transit']
            case 'Received':
                return [__('Received'), 'green', 'status,=,Received']
        }
    }
}