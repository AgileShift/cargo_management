frappe.ui.form.on('Warehouse Receipt', {
	setup(frm) {
		frm.page.sidebar.toggle(false); // Hide Sidebar

		cargo_management.set_transportation_indicator(frm, 'parcel', 'parcel_transportation');
	},

	onload(frm) {
		cargo_management.setup_form_transportation_indicator(frm);
	},

	refresh(frm) {
		if (frm.is_new()) {
			return;
		}

		cargo_management.render_form_transportation_indicator(frm);
	}
});

frappe.ui.form.on('Warehouse Receipt Line', {});
