frappe.ui.form.on('Warehouse Receipt', {
	setup(frm) {
		frm.page.sidebar.toggle(false);

		cargo_management.form_view.set_child_transportation_indicator_formatter(frm, 'parcel', 'parcel_transportation');
	},

	onload(frm) {
		cargo_management.form_view.setup_transportation_indicator(frm);
		// Grid Import applies rows directly and marks the form dirty.
		frm.$wrapper.off('dirty.warehouse_receipt_transportation')
			.on('dirty.warehouse_receipt_transportation', frappe.utils.debounce(() =>
				frm.events.show_transportation_warning(frm), 150));
	},

	refresh(frm) {
		frm.events.show_transportation_warning(frm);
		if (frm.is_new()) {
			return;
		}

		cargo_management.form_view.render_transportation_indicator(frm);
	},

	// Custom Functions
	show_transportation_warning(frm) {
		// The native intro slot may already belong to another message.
		if (frm.$intro_message && frm.$intro_message !== frm.transportation_intro) {
			return;
		}

		const {transportation, warehouse_receipt_lines = []} = frm.doc;
		const opposite = {Air: 'Sea', Sea: 'Air'}[transportation];
		const parcels = warehouse_receipt_lines.filter(row => row.parcel);
		const mismatches = parcels.filter(row => opposite && row.parcel_transportation === opposite);

		if (!mismatches.length) {
			if (frm.transportation_intro) {
				frm.set_intro('');
				frm.transportation_intro = null;
			}
			return;
		}

		const rows = mismatches.slice(0, 5).map(row => row.idx).join(', ');
		const remaining = mismatches.length - 5;
		let message = __('Transportation mismatch: {0} receipt. Rows marked {1}: {2}. Check rows: {3}.', [
			__(transportation), __(opposite), mismatches.length, rows
		]);
		if (remaining > 0) {
			message += ' ' + __('And {0} more.', [remaining]);
		}
		if (mismatches.length === parcels.length) {
			message += ' ' + __('Check Transportation against the PDF.');
		}

		frm.set_intro(message, 'orange');
		frm.transportation_intro = frm.$intro_message;
	}
});

frappe.ui.form.on('Warehouse Receipt Line', {});
