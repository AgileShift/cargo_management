// Personalization for the Parcel List View
frappe.listview_settings['Parcel'] = {

    add_fields: ['status'],
    filters: [
        ['status', '!=', 'finished'],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        // TODO: Finish Indicators
        switch (doc.status) {
            case 'waiting_for_reception':
                return [__('Waiting Reception'), 'blue', 'status,=,waiting_for_reception']
            case 'waiting_confirmation':
                return [__('Waiting Confirmation'), 'orange', 'status,=,waiting_confirmation']
            case 'in_transit':
                return [__('In Transit'), 'purple', 'status,=,in_transit']
            case 'finished':
                return [__('Finished'), 'green', 'status,=,finished']

        }
    }

}