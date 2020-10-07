// Personalization for the Parcel List View
frappe.listview_settings['Parcel'] = {

    add_fields: ['status'],
    filters: [
        ['status', 'not in', ['Finished', 'Cancelled', 'fully_refunded']],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        // TODO: Finish Indicators
        switch (doc.status) {
            case 'Awaiting Receipt':
                return [__('Waiting Reception'), 'blue', 'status,=,waiting_for_reception']
            case 'Awaiting Confirmation':
                return [__('Waiting Confirmation'), 'orange', 'status,=,waiting_confirmation']
            case 'Awaiting Dispatch':
                return [__('Waiting for Departure'), 'yellow', 'status,=,waiting_for_departure']
            case 'In Transit':
                return [__('In Transit'), 'purple', 'status,=,in_transit']
            case 'Finished':
                return [__('Finished'), 'green', 'status,=,finished']

        }
    }

}