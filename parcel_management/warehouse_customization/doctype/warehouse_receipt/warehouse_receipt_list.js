// Personalization for the Package List View
frappe.listview_settings['Warehouse Receipt'] = {
    add_fields: ['status'],
    filters: [
        ['status', '!=', 'Closed'],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        // TODO: Finish Indicators. maybe use the default manager of frappe?
        switch (doc.status) {
            case 'Open':
                return [__('Open'), 'blue', 'status,=,Open']
            case 'In Process':
                return [__('In Process'), 'orange', 'status,=,In Process']
            case 'Closed':
                return [__('Closed'), 'green', 'status,=,Closed']
        }
    }
}