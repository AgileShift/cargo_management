frappe.ui.form.on('Cargo Packing List', {
	refresh: function(frm) {

	    frm.page.add_action_icon('printer', () => {
            frm.print_doc();
	    }, '', __('Print'));

	}
});
