frappe.ui.form.on("Parcel", {

	setup(frm) {},

	onload(frm) {
		cargo_management.setup_form_transportation_indicator(frm);

		$(frm.wrapper)
			.off('dirty.parcel_dirty_ui')
			.on('dirty.parcel_dirty_ui', () => {
				frm.layout.show_message('');      // Clear Message because it's possible that data changes!
				frm.page.clear_custom_actions();  // Clear Custom buttons
			});

		// Setting Currency Labels
		frm.set_currency_labels(['total', 'shipping_amount'], 'USD');
		frm.set_currency_labels(['rate', 'amount'], 'USD', 'content');
	},

	refresh(frm) {
		if (frm.is_new()) {
			return;
		}

		cargo_management.render_form_transportation_indicator(frm); // Add Extra Indicator

		frm.events.show_explained_status(frm); // Show 'Explained Status' as Intro Message
		frm.events.build_custom_actions(frm);  // Adding custom buttons
	},

	tracking_number(frm) {
		frm.doc.tracking_number = frm.doc.tracking_number.trim().toUpperCase();  // Sanitize field

		if (!frm.doc.tracking_number) {
			return;
		}

		frm.doc.carrier = cargo_management.find_carrier_by_tracking_number(frm.doc.tracking_number).carrier;

		refresh_many(['tracking_number', 'carrier']);
	},

	shipping_amount(frm) {
		frm.events.calculate_total(frm);
	},

	// Custom Functions

	show_explained_status(frm) {
		frm.doc.explained_status.message.forEach(m => frm.layout.show_message(m, frm.doc.explained_status.color, true));  // FIXME: Core overrides color
		frm.layout.message.addClass('form-message ' + frm.doc.explained_status.color);
	},

	build_custom_actions(frm) {
		if (frappe.boot.carriers[frm.doc.carrier].api) {
			frm.add_custom_button(__('Get Updates from Carrier'), () => frm.events.get_data_from_api(frm));
		}

		frm.add_custom_button(__('Search'), () => cargo_management.open_carriers_dialog(frm.doc));
	},

	get_data_from_api(frm) {
		// TODO: WORK ON THIS. We have to delete some data
		frappe.call({
			method: 'cargo_management.parcel_management.doctype.parcel.actions.get_data_from_api',
			freeze: true, freeze_message: __('Updating from Carrier...'), args: {source_name: frm.doc.name},
			callback: (r) => {
				// FIXME: "Not Saved" indicator cannot be changed.
				console.log('Need to work in here. problems in v14');
				//frappe.model.sync(r.message);
				//frm.refresh();
			}
		});
	},

	calculate_total(frm) {
		frm.set_value('total', frm.get_sum('content', 'amount') + frm.doc.shipping_amount);
	},
	calculate_content_amounts_and_total(frm, cdt, cdn) {
		let row = locals[cdt][cdn]; // Getting Content Child Row being edited

		row.amount = row.qty * row.rate;
		refresh_field('amount', cdn, 'content');

		frm.events.calculate_total(frm); // Calculate the parent 'total' field
	}
});

frappe.ui.form.on('Parcel Content', {
	content_remove(frm) {
		frm.events.calculate_total(frm);
	},

	qty(frm, cdt, cdn) {
		frm.events.calculate_content_amounts_and_total(frm, cdt, cdn);
	},

	rate(frm, cdt, cdn) {
		frm.events.calculate_content_amounts_and_total(frm, cdt, cdn);
	},
});
// 201 - FIXME: Giving PROBLEMS
// 254 -> Working on Frappe Boot Info for Carriers!
