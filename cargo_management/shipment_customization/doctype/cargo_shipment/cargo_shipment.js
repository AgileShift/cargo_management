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
                frappe.utils.play_sound('click');  // Really Necessary?
                frappe.call({
                    method: 'cargo_management.shipment_customization.doctype.cargo_shipment.actions.mark_cargo_shipment_in_transit',
                    args: {source_name: frm.doc.name}
                });
            });
        } else {
            frm.page.clear_actions_menu();
        }

        // TODO: Add intro message for helper!
    }
});
