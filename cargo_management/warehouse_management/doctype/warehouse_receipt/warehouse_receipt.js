function show_warehouse_receipt_transportation_warning(frm) {
	const {transportation, warehouse_receipt_lines = []} = frm.doc;
	const rows = warehouse_receipt_lines.filter(row => row.parcel);
	const opposite = {Air: 'Sea', Sea: 'Air'}[transportation];
	const mismatches = opposite ? rows.filter(row => row.parcel_transportation === opposite) : [];
	const current_intro = frm.$intro_message;
	const owns_intro = current_intro && current_intro === frm.warehouse_receipt_transportation_intro;

	// Frappe has one intro slot. Leave a different intro alone.
	if (current_intro && !owns_intro) {
		return;
	}
	if (!mismatches.length) {
		if (owns_intro) {
			frm.set_intro('');
			frm.warehouse_receipt_transportation_intro = null;
		}
		return;
	}

	const row_limit = 5;
	const row_numbers = mismatches.slice(0, row_limit).map(row => row.idx).join(', ');
	const remaining = mismatches.length - row_limit;
	const receipt_mode = __(transportation);
	const parcel_mode = __(opposite);
	let message = mismatches.length === 1
		? __('Transportation mismatch: this receipt is {0}, but 1 row shows {1}. Check row {2}.', [
			receipt_mode, parcel_mode, row_numbers,
		])
		: __('Transportation mismatch: this receipt is {0}, but {1} rows show {2}. Check rows: {3}.', [
			receipt_mode, mismatches.length, parcel_mode, row_numbers,
		]);
	if (remaining > 0) {
		message += ' ' + __('And {0} more.', [remaining]);
	}
	if (mismatches.length === rows.length) {
		message += ' ' + __('All listed parcels show {0}. Check Transportation against the PDF.', [
			parcel_mode,
		]);
	}

	frm.set_intro(message, 'orange');
	frm.warehouse_receipt_transportation_intro = frm.$intro_message;
}

frappe.ui.form.on('Warehouse Receipt', {
	setup(frm) {
		frm.page.sidebar.toggle(false);

		cargo_management.form_view.set_child_transportation_indicator_formatter(frm, 'parcel', 'parcel_transportation');
	},

	onload(frm) {
		cargo_management.form_view.setup_transportation_indicator(frm);
		// Grid Import applies rows directly and marks the form dirty.
		frm.$wrapper.off('dirty.warehouse_receipt_transportation')
			.on('dirty.warehouse_receipt_transportation', frappe.utils.debounce(() => {
				show_warehouse_receipt_transportation_warning(frm);
			}, 150));
	},

	refresh(frm) {
		show_warehouse_receipt_transportation_warning(frm);
		if (frm.is_new()) {
			return;
		}

		cargo_management.form_view.render_transportation_indicator(frm);
	},

	transportation: show_warehouse_receipt_transportation_warning
});

frappe.ui.form.on('Warehouse Receipt Line', {
	parcel: show_warehouse_receipt_transportation_warning,
	parcel_transportation: show_warehouse_receipt_transportation_warning,
	warehouse_receipt_lines_add: show_warehouse_receipt_transportation_warning,
	warehouse_receipt_lines_remove: show_warehouse_receipt_transportation_warning
});
