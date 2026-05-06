frappe.ui.form.on('Warehouse Receipt', {
	setup(frm) {
		frm.page.sidebar.toggle(false); // Hide Sidebar
	}
});

frappe.ui.form.on('Warehouse Receipt Line', {});
