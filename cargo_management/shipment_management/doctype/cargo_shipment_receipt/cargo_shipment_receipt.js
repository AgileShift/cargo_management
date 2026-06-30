frappe.ui.form.on('Cargo Shipment Receipt', {
	// TODO: On Save set customer on the parcel that are not set!

	setup(frm) {
		frm.page.sidebar.toggle(false); // Hide Sidebar

		cargo_management.set_transportation_indicator(frm, 'parcel');
	},

	onload: function (frm) {
		cargo_management.setup_form_transportation_indicator(frm);

		// TODO: Set Query for cargo_shipment_receipt_warehouse_lines

		// Adding the two possible ways to trigger a fetch for customer_name : FIXME REVIEW THIS!. what happens on multiple customers same tracking?
		frm.add_fetch('parcel', 'customer_name', 'customer_name');
		frm.add_fetch('customer', 'customer_name', 'customer_name');
	},

	refresh: function (frm) {
		// TODO: after UI release: Child table dont update after save(validate method sorts the child table)
		// TODO: Add a button to sort child table by customer name.
		// TODO: Add intro message when the cargo shipment is on a cargo shipment receipt
		// TODO: Add Progress: dashboard.add_progress or frappe.chart of type: percentage
		if (frm.is_new()) {
			return;
		}

		cargo_management.render_form_transportation_indicator(frm);

		if (frm.doc.status === 'Awaiting Receipt') { // Awaiting or actually sorting
			frm.page.add_action_item(__('Mark as Sorting'), () => {
				frappe.call({
					method: 'cargo_management.engine.status_update.update_cargo_shipment_receipt_status',
					freeze: true,
					args: {
						source_doc_name: frm.doc.name,
						new_status: 'Sorting',
						msg_title: __('Marked as Sorting')
					}
				}); // TODO: Refresh DOC in callback
			});
		} else if (frm.doc.status === 'Sorting') {
			frm.add_custom_button(__('Sales Invoice'), () => {
				frappe.call({
					method: 'cargo_management.engine.sales_invoice.make_sales_invoice_from_cargo_shipment_receipt',
					args: {doc: frm.doc},
					freeze: true,
					freeze_message: __('Creating Sales Invoice...')
				});//.then(r => { // Return customers invoices
				// frm.refresh_field('cargo_shipment_receipt_lines');
				// });
			}, __('Create'));

			frm.page.set_inner_btn_group_as_primary(__('Create'));
		} else {
			frm.page.clear_actions_menu();
		}
	},

	cargo_shipment: function (frm) {
		if (!frm.doc.cargo_shipment) {
			return;
		}

		// We clear the table each time to avoid duplication
		frm.clear_table('cargo_shipment_receipt_lines');

		frappe.call({
			method: 'cargo_management.shipment_management.utils.get_parcels_and_wr_in_cargo_shipment',
			type: 'GET',
			args: {cargo_shipment: frm.doc.cargo_shipment},
			freeze: true,
			freeze_message: __('Adding Parcels...'),
		}).then(r => {

			r.message.parcels.forEach(parcel => {
				frm.add_child('cargo_shipment_receipt_lines', {
					'content': parcel.customer_description,
					// 'item_code': parcel.item_code, TODO: This is not working, because the parcel can have more than once item code

					'customer': parcel.customer,
					'customer_name': parcel.customer_name,

					'parcel': parcel.name,
					'parcel_2': parcel.tracking_number,
					'carrier_est_weight': parcel.carrier_est_weight,

					'assisted_purchase': parcel.assisted_purchase,
					'transportation': parcel.transportation,
					'shipper': parcel.shipper,
				});
			});

			// Refresh the modified tables inside the callback after execution is done
			frm.refresh_field('cargo_shipment_receipt_lines');
		});
	},
});

frappe.ui.form.on('Cargo Shipment Receipt Line', {
	// TODO: We should allow always customer to be read not read_only?
	// TODO: Add a button to trigger this info!
	// TODO ADD Extra Info: Warehouse Weight, Carrier Weight, Gross Weight:
	// TODO: This can be improved more dynamically -> // HELPERS -> Fix or Make more Dynamic

	form_render: function (frm, cdt, cdn) {
		const row = frm.fields_dict.cargo_shipment_receipt_lines.grid.grid_rows_by_docname[cdn];

		if (!row?.grid_form?.fields_dict?.item_code) {
			return;
		}

		row.grid_form.wrapper.find('.item-code-shortcuts').remove();

		const shortcuts = $(`
			<div class="item-code-shortcuts form-group">
				<div class="item-code-shortcuts-header">${__('Shortcuts')}</div>
				<div class="item-code-shortcuts-list"></div>
			</div>
		`);
		const button_group = shortcuts.find('.item-code-shortcuts-list');

		$('<button class="btn btn-xs btn-default item-code-shortcut" type="button"></button>')
			.text('1 LB')
			.on('click', () => { // Set Default Weight
				locals[cdt][cdn].gross_weight = 1.00;
				refresh_field('gross_weight', cdn, 'cargo_shipment_receipt_lines');
				frm.dirty();
			}).appendTo(button_group);

		// TODO: This can be improved more dynamically -> // HELPERS -> Fix or Make more Dynamic
		[
			'IP Varios - PESO',
			'IP Ropa - PESO',
			'IP Zapatos - PESO',
			'IP Cosméticos - PESO',
			'IP Skincare - PESO',
			'IP Perfumes - PESO',
			'IP Peluches - PESO',
			'IP Juguetes - PESO',
			'IP Reloj - PESO',
			'IP Electronico - PESO',
			'IP Salud y Hogar - PESO',
			'IP Vitaminas y Suplementos - PESO',
			'IP Repuestos - PESO',
			'IP Repuesto Auto - PESO',
			'IP Repuesto de Moto - PESO'
		].forEach(item_code => {
			$('<button class="btn btn-xs btn-default item-code-shortcut" type="button"></button>')
				.text(item_code.replace('IP ', ''))
				.attr('title', item_code)
				.on('click', () => {
					locals[cdt][cdn].item_code = item_code;  // Getting Content Child Row being edited
					refresh_field('item_code', cdn, 'cargo_shipment_receipt_lines');
					frm.dirty();
				}).appendTo(button_group);
		});

		row.grid_form.fields_dict.section_break_bhmz.wrapper.after(shortcuts);

		button_group.css({
			'display': 'grid',
			'grid-template-columns': 'repeat(auto-fit, minmax(170px, 1fr))',
			'gap': '8px',
			'align-items': 'center'
		});
	},

	item_code: function (frm, cdt, cdn) {
		const item = locals[cdt][cdn];

		if (item.item_code.includes('FIJO')) { // FIXME: HOTFIX -> 7 March 2025 # Employee added 1 to the billable qty
			frm.fields_dict['cargo_shipment_receipt_lines'].grid.update_docfield_property('billable_qty_or_weight', 'hidden', false);
		} else {
			frm.fields_dict['cargo_shipment_receipt_lines'].grid.update_docfield_property('billable_qty_or_weight', 'hidden', true);
		}
	},
});
// 148, my code is garbage
