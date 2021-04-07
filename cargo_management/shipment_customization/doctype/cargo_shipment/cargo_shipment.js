frappe.ui.form.on('Cargo Shipment', {

    // TODO: Formatter for warehouse receipt item?

    onload: function(frm) {
        frm.set_query('cargo_shipment_lines', () => {
            return {
                filters: {status: 'Awaiting Departure'}
            }
        });
    },

    refresh: function(frm) {
        // TODO: Add intro message when the cargo shipment is on a cargo shipment receipt
        // TODO: Add Progress: dashboard.add_progress or frappe.chart of type: percentage

        if (frm.is_new()) {
            return;
        }

        if (frm.doc.status === 'Awaiting Departure') {
            frm.page.add_action_item(__('Confirm Transit'), () => {
                frappe.call({
                    method: 'cargo_management.shipment_customization.doctype.cargo_shipment.actions.update_status',
                    freeze: true,
                    args: {
                        source_doc_name: frm.doc.name,
                        new_status: 'In Transit'
                    }
                });
            });
        } else {
            frm.page.clear_actions_menu();
        }
    }
});
