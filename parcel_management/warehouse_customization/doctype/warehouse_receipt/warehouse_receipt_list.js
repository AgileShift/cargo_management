// Personalization for the Package List View
frappe.listview_settings['Warehouse Receipt'] = {
    add_fields: ['status'],
    filters: [
        ['status', '!=', 'CLOSED'],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        // TODO: Finish Indicators. maybe use the default manager of frappe?
        switch (doc.status) {
            case 'DRAFT':
                return [__('Draft'), 'orange', 'status,=,DRAFT']
            case 'OPEN':
                return [__('Open'), 'blue', 'status,=,OPEN']
            case 'CLOSED':
                return [__('Closed'), 'green', 'status,=,CLOSED']
            case 'RECEIVED':
                return [__('Received'), 'green', 'status,=,RECEIVED']
        }
    }
}