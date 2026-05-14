frappe.ui.form.on('Warehouse Receipt', {
	setup(frm) {
		frm.page.sidebar.toggle(false); // Hide Sidebar

		cargo_management.set_transportation_indicator(frm, 'parcel', 'parcel_transportation');
	}
});

frappe.ui.form.on('Warehouse Receipt Line', {});
