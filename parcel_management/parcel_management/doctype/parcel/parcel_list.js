frappe.listview_settings['Parcel'] = {
    add_fields: ['status'],
    filters: [
        ['status', 'not in', ['Finished', 'Cancelled', 'fully_refunded']],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        // TODO: Finish Indicator
        switch (doc.status) {
            case 'Awaiting Receipt':
                return [__('Awaiting Receipt'), 'blue', 'status,=,Awaiting Receipt']
            case 'Awaiting Confirmation':
                return [__('Awaiting Confirmation'), 'orange', 'status,=,Awaiting Confirmation']
            case 'In Extraordinary Confirmation':
                return [__('In Extraordinary Confirmation'), 'red', 'status,=,In Extraordinary Confirmation']
            case 'Awaiting Departure':
                return [__('Awaiting Departure'), 'yellow', 'status,=,Awaiting Departure']
            case 'In Transit':
                return [__('In Transit'), 'purple', 'status,=,In Transit']
            case 'In Customs':
                return [__('In Customs'), 'black', 'status,=,In Customs']
            case 'Sorting':
                return [__('Sorting'), 'black', 'status,=,Sorting']
            case 'Available to Pickup':
                return [__('Available to Pickup'), 'green', 'status,=,Available to Pickup']
            case 'Finished':
                return [__('Finished'), 'green', 'status,=,Finished']
            case 'Cancelled':
                return [__('Cancelled'), 'red', 'status,=,Cancelled']
        }
    }

}