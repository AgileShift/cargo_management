frappe.ui.form.on('Parcel', {

	setup(frm) {
		frm.page.sidebar.toggle(false); // Hide Sidebar

		// FIXME: Observe if the indicator changes. This is useful for the 'Not Saved' status aka is_dirty(). We cannot read that from the events available
		const observer = new MutationObserver(() => {
			frm.layout.show_message('');     // Clear Message because it's possible that data changes!
			frm.page.clear_custom_actions(); // Clear Custom buttons
			frm.page.indicator.next().remove(); // Remove the extra indicator if the indicator changes
		});

		observer.observe(frm.page.indicator.get(0), {childList: true}); // Observe the 'indicator' for changes
	},

	onload(frm) {
		// Setting custom queries
		frm.set_query('item_code', 'content', () => {
			return {
				filters: {
					'is_sales_item': true,
					'has_variants': false
				}
			}
		});

		// Setting Currency Labels
		frm.set_currency_labels(['total', 'shipping_amount'], 'USD');
		frm.set_currency_labels(['rate', 'amount'], 'USD', 'content');
	},

	refresh(frm) {
		if (frm.is_new()) {
			return;
		}

		frm.page.indicator.parent().append(cargo_management.transportation_indicator(frm.doc.transportation)); // Add Extra Indicator

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
		frm.doc.explained_status.message.forEach(m => frm.layout.show_message(m, ''));  // FIXME: Core overrides color
		frm.layout.message.removeClass().addClass('form-message ' + frm.doc.explained_status.color);
	},

	build_custom_actions(frm) {
		const carriers_settings = cargo_management.load_carrier_settings(frm.doc.carrier);

		if (carriers_settings.api) {
			frm.add_custom_button(__('Get Updates from Carrier'), () => frm.events.get_data_from_api(frm));
		}

		if (frm.doc.assisted_purchase) { // If is Assisted Purchase will have related Sales Order and Sales Order Item
			frm.add_custom_button(__('Sales Order'), () => frm.events.sales_order_dialog(frm), __('Get Items From'));
		}

		carriers_settings.urls.forEach(url => frm.add_custom_button(url.title, () => window.open(url.url + frm.doc.tracking_number)));
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

	//https://github.com/frappe/frappe/pull/12471 and https://github.com/frappe/frappe/pull/14181/files
	sales_order_dialog(frm) {
		const so_dialog = new frappe.ui.form.MultiSelectDialog({
			doctype: 'Sales Order',
			target: frm,
			setters: {
				delivery_date: undefined,
				status: undefined
			},
			add_filters_group: 1,
			get_query: () => {
				return {
					filters: {  // TODO: Only uncompleted orders!
						docstatus: 1,
						customer: frm.doc.customer,
					}
				};
			},
			action: (selections) => {
				if (selections.length === 0) {
					frappe.msgprint(__("Please select {0}", [so_dialog.doctype]))
					return;
				}
				// so_dialog.dialog.hide();
				frm.events.so_items_dialog(frm, selections);
			}
		});
	},

	so_items_dialog: async function (frm, sales_orders) {
		// Getting all sales order items from Sales Order
		let sale_order_items = await frappe.db.get_list('Sales Order Item', {
			filters: {'parent': ['in', sales_orders]},
			fields: ['name as docname', 'item_code', 'description', 'qty', 'rate']
		});

		const so_items_dialog = new frappe.ui.form.MultiSelectDialog({
			doctype: 'Sales Order Item',
			target: frm,
			setters: {
				// item_code: undefined,
				// qty: undefined,
				// rate: undefined
			},
			data_fields: [
				{
					fieldtype: 'Currency',
					options: "USD",
					fieldname: "rate",
					read_only: 1,
					hidden: 1,
				},
				{
					fieldname: 'item_code',
					fieldtype: 'Data',
					label: __('Item sshhshsh')
				}],
			get_query: () => {
				return {
					filters: {
						parent: ['in', sales_orders]
					}
				}
			},
			add_filters_group: 1,
			action: (jkjk) => {
				console.log(jkjk);
			},
			primary_action_label: __('Select')
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
//201 - FIXME: Giving PROBLEMS
