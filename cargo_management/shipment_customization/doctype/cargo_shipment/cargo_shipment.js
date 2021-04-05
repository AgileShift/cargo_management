frappe.ui.form.on('Cargo Shipment', {

    onload: function(frm) {
        frm.set_query('cargo_shipment_lines', () => {
            return {
                filters: {status: 'Open'}
            }
        });
    },

    refresh: function(frm) {
        if (frm.is_new()) {
            return;
        }

        if (frm.doc.status === 'Open') {
            frm.page.add_action_item(__('Confirm Transit'), () => {
                frappe.call({
                    method: 'cargo_management.package_management.doctype.package.actions.update_status',
                    args: {
                        source_doc: frm.doc,
                        action: 'confirm_transit'
                    }
                });
            });
        } else {
            frm.page.clear_actions_menu();
        }

        // TODO: Add intro message for helper!
    }
});
