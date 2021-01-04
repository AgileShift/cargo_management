frappe.ui.form.on('Cargo Shipment', {

    setup: function (frm) {
        // TODO: this must be running from core frappe code. Some glitch make us hardcoded the realtime handler here.
        frappe.realtime.on('doc_update', () => { // See: https://github.com/frappe/frappe/pull/11137
            frm.reload_doc(); // Reload form UI data from db.
        });
    },

    onload: function(frm) {
        frm.set_query('cargo_shipment_lines', () => {
            return {
                filters: {
                    status: 'Open'
                }
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
                    method: 'package_management.shipment_customization.doctype.cargo_shipment.actions.mark_cargo_shipment_in_transit',
                    args: {source_name: frm.doc.name}
                });
            });
        } else {
            frm.page.clear_actions_menu();
        }

        // TODO: Add intro message for helper!
    }
});
