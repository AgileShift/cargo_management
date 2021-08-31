frappe.ui.form.on('Warehouse Receipt', {

    // setup: function (frm) {
        // TODO: formatter for package item?
		// frm.set_indicator_formatter('package', (doc) => {
		//     return (doc.status==='In Transit') ? "green" : "orange"
		// });
    // },

    onload: function (frm) {
	    frm.set_query('package', 'warehouse_receipt_lines', () => {
            return {
                filters: {
                    status: ['not in', ['Awaiting Departure', 'In Transit', 'In Customs', 'Sorting', 'Available to Pickup', 'Finished']]
                }
            };
        });
    },

    refresh: function (frm) {
        // TODO: Add intro message when the warehouse is on cargo_shipment!
        // TODO: Add Progress: dashboard.add_progress or frappe.chart of type: percentage

        if (frm.is_new()) {
            return;
        }

        // TODO: Work on this
        if (frm.doc.status === 'Awaiting Departure') {
            frm.page.add_action_item(__('Confirm Packages'), () => {
                frappe.call({
                    method: 'cargo_management.warehouse_management.doctype.warehouse_receipt.actions.update_status',
                    freeze: true,
                    args: {
                        source_doc_name: frm.doc.name,
                        new_status: 'Awaiting Departure'
                    }
                });
            });
        }// else {
            // frm.page.clear_actions_menu();  # TODO
        // }
    },

    before_save: function (frm) {
        // Calculate fields from child so can be saved from client-side
        frm.set_value('warehouse_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'warehouse_est_weight'));
        frm.set_value('carrier_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'carrier_est_weight'));
    }
});
