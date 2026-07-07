frappe.ui.form.on('Warehouse Receipt', {
	setup(frm) {
		frm.page.sidebar.toggle(false); // Hide Sidebar

		cargo_management.form_view.set_child_transportation_indicator_formatter(frm, 'parcel', 'parcel_transportation');
	},

	onload(frm) {
		cargo_management.form_view.setup_transportation_indicator(frm);
	},

	refresh(frm) {
		if (frm.is_new()) {
			return;
		}

		cargo_management.form_view.render_transportation_indicator(frm);
	}
});

frappe.ui.form.on('Warehouse Receipt Line', {});
