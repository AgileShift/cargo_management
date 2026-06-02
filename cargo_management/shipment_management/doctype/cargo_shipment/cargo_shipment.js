frappe.ui.form.on('Cargo Shipment', {
	setup(frm) {
		frm.page.sidebar.toggle(false); // Hide Sidebar

		cargo_management.set_transportation_indicator(frm, 'warehouse_receipt');
		cargo_management.set_transportation_indicator(frm, 'parcel');
	},

	onload(frm) {},

	refresh: function (frm) {
		if (frm.is_new()) {
			return;
		}
		
		// TODO: Add intro message when the cargo shipment is on a cargo shipment receipt
		// TODO: Add Progress: dashboard.add_progress or frappe.chart of type: percentage
		frm.page.indicator.parent().append(cargo_management.transportation_indicator(frm.doc.transportation));

		frm.events.build_custom_action_items(frm); // Adding Custom Action Items
	},

	validate: function (frm) {
		frm.doc.pieces = frm.doc.cargo_shipment_lines.length;

		frm.doc.estimated_gross_weight_by_warehouse_in_pounds = frm.get_sum('warehouse_lines', 'weight');
		frm.doc.estimated_gross_weight_by_carriers_in_pounds = frm.get_sum('cargo_shipment_lines', 'carrier_est_weight');
	},

	build_custom_action_items(frm) {
		if (frm.doc.status === 'Awaiting Departure') {
			frm.page.add_action_item(__('Confirm Parcels'), () => {
				frappe.call({
					method: 'cargo_management.shipment_management.doctype.cargo_shipment.actions.update_status',
					freeze: true,
					args: {
						source_doc_name: frm.doc.name,
						new_status: 'Awaiting Departure',
						msg_title: __('Confirmed Parcels')
					}
				});
			});

			frm.page.add_action_item(__('Confirm Transit'), () => {
				frappe.call({
					method: 'cargo_management.shipment_management.doctype.cargo_shipment.actions.update_status',
					freeze: true,
					args: {
						source_doc_name: frm.doc.name,
						new_status: 'In Transit',
						msg_title: __('Now in Transit')
					} // TODO: Refresh DOC in callback
				});
			});
		} else {
			frm.page.clear_actions_menu();
		}
	}
});


frappe.ui.form.on('Cargo Shipment Warehouse', {});
