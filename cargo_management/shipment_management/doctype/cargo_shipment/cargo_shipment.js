frappe.ui.form.on('Cargo Shipment', {
	setup(frm) {
		frm.page.sidebar.toggle(false); // Hide Sidebar

		cargo_management.form_view.set_child_transportation_indicator_formatter(frm, 'warehouse_receipt');
		cargo_management.form_view.set_child_transportation_indicator_formatter(frm, 'parcel');
	},

	onload(frm) {
		cargo_management.form_view.setup_transportation_indicator(frm);
	},

	refresh: function (frm) {
		if (frm.is_new()) {
			return;
		}

		// TODO: Add intro message when the cargo shipment is on a cargo shipment receipt
		// TODO: Add Progress: dashboard.add_progress or frappe.chart of type: percentage
		cargo_management.form_view.render_transportation_indicator(frm);

		frm.events.build_custom_action_items(frm); // Adding Custom Action Items
	},

	validate: function (frm) {
		frm.doc.pieces = frm.doc.cargo_shipment_lines.length;

		frm.doc.estimated_gross_weight_by_warehouse_in_pounds = frm.get_sum('warehouse_lines', 'weight');
		frm.doc.estimated_gross_weight_by_carriers_in_pounds = frm.get_sum('cargo_shipment_lines', 'carrier_est_weight');
	},

	build_custom_action_items(frm) {
		if (frm.doc.status === 'Awaiting Departure') {
			frm.events.add_status_action(frm, __('Confirm Parcels'), 'Awaiting Departure', __('Confirmed Parcels'));
			frm.events.add_status_action(frm, __('Confirm Transit'), 'In Transit', __('Now in Transit'));
		} else {
			frm.page.clear_actions_menu();
		}
	},

	add_status_action(frm, label, new_status, msg_title) {
		frm.page.add_action_item(label, () => {
			frappe.call({
				method: 'cargo_management.engine.status_update.update_cargo_shipment_status',
				freeze: true,
				args: {
					source_doc_name: frm.doc.name,
					new_status,
					msg_title
				}
			}); // TODO: Refresh DOC in callback
		});
	}
});

frappe.ui.form.on('Cargo Shipment Warehouse', {});
