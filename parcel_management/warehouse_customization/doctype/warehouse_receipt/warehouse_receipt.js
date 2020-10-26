frappe.ui.form.on('Warehouse Receipt', {

    onload: function (frm) {

	    frm.set_query('warehouse_receipt_lines', () => {
            return {
                'filters': [
                    ['Parcel', 'status', 'not in', ['Available to Pickup', 'Finished']]
                ]
            };
        });

    },

    refresh: function (frm) {

        if (frm.is_new()) {
            return;
        }

        // Adding the confirm parcel button if warehouse receipt is open
        if (frm.doc.status === 'Open') {
            frm.page.add_action_item(__('Confirm Parcels'), () => {
                frappe.utils.play_sound('click');  // Really Necessary?
                frappe.call({
                    method: 'parcel_management.warehouse_customization.doctype.warehouse_receipt.actions.confirm_parcels',
                    args: {doc: frm.doc}
                })
            });
        }
    },

});
