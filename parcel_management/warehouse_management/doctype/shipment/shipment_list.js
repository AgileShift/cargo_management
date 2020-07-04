frappe.listview_settings['Shipment'] = {
    add_fields: ['status'],
    filters: [
        ['status', '!=', 'RECEIVED'],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        // TODO: Finish Indicators
        switch (doc.status) {
            case 'LOADING':
                return [__('Draft'), 'orange', 'status,=,LOADING']
            case 'IN_TRANSIT':
                return [__('Open'), 'blue', 'status,=,IN_TRANSIT']
            case 'RECEIVED':
                return [__('Closed'), 'green', 'status,=,RECEIVED']
        }
    }
}