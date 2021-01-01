frappe.ui.form.on('Warehouse Receipt', {

    setup: function (frm) {
        // TODO: this must be running from core frappe code. Some glitch make us hardcoded the realtime handler here.
        frappe.realtime.on('doc_update', () => { // See: https://github.com/frappe/frappe/pull/11137
            frm.reload_doc(); // Reload form UI data from db.
        });
    },

    onload: function (frm) {
	    frm.set_query('warehouse_receipt_lines', () => {
            return {
                'filters': [
                    ['Package', 'status', 'not in', ['Available to Pickup', 'Finished']]
                ]
            };
        });
    },

    refresh: function (frm) {
        if (frm.is_new()) {
            return;
        }

        if (frm.doc.status === 'Open') {
            frm.page.add_action_item(__('Confirm Packages'), () => {
                frappe.utils.play_sound('click');  // Really Necessary?
                frappe.call({
                    method: 'cargo_management.warehouse_customization.doctype.warehouse_receipt.actions.confirm_packages_in_wr',
                    args: {doc: frm.doc}
                });
            });
        } else {
            frm.page.clear_actions_menu();
        }

        // TODO: Add intro message when the warehouse is on shipment!
    },

});
