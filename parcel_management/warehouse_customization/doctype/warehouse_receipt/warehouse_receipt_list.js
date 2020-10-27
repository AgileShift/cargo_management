frappe.listview_settings['Warehouse Receipt'] = {
    add_fields: ['status'],
    filters: [
        ['status', '!=', 'Closed'],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        switch (doc.status) {
            case 'Open':
                return [__('Open'), 'blue', 'status,=,Open']
            case 'In Transit':
                return [__('In Transit'), 'orange', 'status,=,In Transit']
            case 'Closed':
                return [__('Closed'), 'green', 'status,=,Closed']
        }
    }
}