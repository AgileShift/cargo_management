frappe.ui.form.on('Warehouse Receipt', {
	setup(frm) {
		frm.page.sidebar.toggle(false); // Hide Sidebar

		cargo_management.set_transportation_indicator(frm, 'parcel', 'parcel_transportation');
	},

	before_save(frm) {
		if (!should_prompt_for_single_line_copy(frm))
			return;

		return new Promise((resolve) => {
			frappe.confirm(
				__('This Warehouse Receipt has one parcel line. Copy package type and dimensions from the line to the Warehouse Receipt?'),
				() => frm.set_value('copy_single_line_details', 1).then(resolve),
				resolve
			);
		});
	}
});

frappe.ui.form.on('Warehouse Receipt Line', {});

function should_prompt_for_single_line_copy(frm) {
	const line = frm.doc.warehouse_receipt_lines?.[0];

	if (!line || frm.doc.warehouse_receipt_lines.length !== 1 || frm.doc.copy_single_line_details)
		return false;

	return frm.doc.type !== line.package_type
		|| flt(frm.doc.length) !== flt(line.length)
		|| flt(frm.doc.width) !== flt(line.width)
		|| flt(frm.doc.height) !== flt(line.height);
}
