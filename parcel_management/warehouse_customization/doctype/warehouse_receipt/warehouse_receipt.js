// Copyright (c) 2020, Agile Shift and contributors
// For license information, please see license.txt

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

        // Adding the confirm parcel button if warehouse receipt is open
        if (frm.doc.status === 'Open') {
            frm.page.add_action_item(__('Confirm Parcels'), () => {
                frappe.msgprint("Confirmando Paquetes");
            });
        }
    },

});
