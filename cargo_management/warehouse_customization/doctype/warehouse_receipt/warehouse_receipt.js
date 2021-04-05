frappe.ui.form.on('Warehouse Receipt', {

    setup: function (frm) {
        // TODO: formatter for package item?
		// frm.set_indicator_formatter('package', (doc) => {
		//     return (doc.status==='In Transit') ? "green" : "orange"
		// });
    },

    onload: function (frm) {
	    frm.set_query('package', 'warehouse_receipt_lines', () => {
            return {
                filters: {
                    status: ['not in', ['Available to Pickup', 'Finished']]
                }
            };
        });
    },

    refresh: function (frm) {
        if (frm.is_new()) {
            return;
        }

        // TODO: Work on this
        if (frm.doc.status === 'Open') {
            frm.page.add_action_item(__('Confirm Packages'), () => {
                frappe.call({
                    method: 'cargo_management.warehouse_customization.doctype.warehouse_receipt.actions.update_status',
                    args: {
                        doc: frm.doc,
                        new_status: 'Awaiting Departure'
                    }
                });
            });
        }// else {
            // frm.page.clear_actions_menu();
        // }

        // TODO: Add intro message when the warehouse is on cargo_shipment!
        // TODO: Add Progress: dashboard.add_progress or frappe.chart of type: percentage
    },

});
