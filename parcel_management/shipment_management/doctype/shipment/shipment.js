frappe.ui.form.on('Shipment', {

    refresh: function(frm) {
        if (frm.is_new()) {
            return;
        }

        if (frm.doc.status === 'Open') {
            frm.page.add_action_item(__('Confirm Transit'), () => {
                frappe.utils.play_sound('click');  // Really Necessary?
                frappe.call({
                    method: 'parcel_management.shipment_management.doctype.shipment.actions.mark_shipment_in_transit',
                    args: {doc: frm.doc}
                });
            });
        }

    }
});
