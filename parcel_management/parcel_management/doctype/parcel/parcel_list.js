// Personalization for the Parcel List View
frappe.listview_settings['Parcel'] = {
    // Add fields to fetch
    add_fields: ['status'],

    // Setting default filters
    filters: [
        ['status', 'not in', ['Finished', 'Cancelled', 'fully_refunded']],
    ],
    hide_name_column: true, // Hide the last column which shows the `name`

    get_indicator(doc) {  // customize indicator color
        // TODO: Finish Indicators
        switch (doc.status) {
            case 'Awaiting Receipt':
                return [__('Awaiting Receipt'), 'blue', 'status,=,Awaiting Receipt']
            case 'Awaiting Confirmation':
                return [__('Awaiting Confirmation'), 'orange', 'status,=,Awaiting Confirmation']
            case 'Awaiting Dispatch':
                return [__('Awaiting Dispatch'), 'yellow', 'status,=,Awaiting Dispatch']
            case 'In Transit':
                return [__('In Transit'), 'purple', 'status,=,In Transit']
            case 'Finished':
                return [__('Finished'), 'green', 'status,=,Finished']
            case 'Cancelled':
                return [__('Cancelled'), 'red', 'status,=,Cancelled']

        }
    }

}