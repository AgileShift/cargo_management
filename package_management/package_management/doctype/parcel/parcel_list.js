frappe.listview_settings['Parcel'] = {
    add_fields: ['status', 'carrier'],
    filters: [
        ['status', 'not in', ['Finished', 'Cancelled', 'fully_refunded']],
    ],
    hide_name_column: true,

    get_indicator(doc) {
        const status_color = {
            'Awaiting Receipt': 'blue',
            'Awaiting Confirmation': 'orange',
            'In Extraordinary Confirmation': 'red',
            'Awaiting Departure': 'yellow',
            'In Transit': 'purple',
            'In Customs': 'black',
            'Sorting': 'black',
            'Available to Pickup': 'green',
            'Finished': 'green',
            'Cancelled': 'red',
        };

        return [__(doc.status), status_color[doc.status], 'status,=,' + doc.status];
    },

    onload: function (listview) {
        listview.page.add_actions_menu_item(__('Update data from carrier'), function () {
            // TODO FINISH.... This is work in progress
            // Bulk Dialog - should sent email if status is changed?
            // Bulk show_progress. This actually reloads the form? if so. how many times?
            listview.call_for_selected_items(
                'package_management.package_management.doctype.parcel.actions.update_data_from_carrier_bulk'
            );
        })

    },

    button: {
        show(doc) {
            return doc.name;
        },
        get_label() {
            return __('Carrier page')
        },
        get_description() {
            return __('Visit carrier detail page')
        },
        action(doc) {
            frappe.utils.play_sound('click');  // Really Necessary?
            frappe.call({
                method: 'package_management.package_management.doctype.parcel.actions.get_carrier_detail_page_url',
                args: {carrier: doc.carrier},
                callback: (r) => {
                    window.open(r.message + doc.tracking_number, '_blank');
                }
            });
        },
    },
}
