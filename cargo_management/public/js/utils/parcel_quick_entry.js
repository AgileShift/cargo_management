frappe.provide('frappe.ui.form');

frappe.ui.form.ParcelQuickEntryForm = class ParcelQuickEntryForm extends frappe.ui.form.QuickEntryForm {
	constructor(doctype, after_insert, init_callback, doc, force) {
		super(doctype, after_insert, init_callback, doc, force);
	}

	render_dialog() {
		// FIXME: Look For a Place to Override Parcel Form Control
		frappe.meta.docfield_map['Parcel']['transportation'].fieldtype = 'TransportationMultiCheck';

		this.add_extra_fields(); // Adding Table Field after executing super.is_quick_entry();
		super.render_dialog();
		this.init_post_render_dialog_operations(); // Custom method to modify DOM properties after the dialog has been rendered

		frappe.meta.docfield_map['Parcel']['transportation'].fieldtype = 'Select'; // FIXME: Resetting the fieldtype to 'Select' to avoid problems in other parts of the system(ListView Filter and Form Field)
	}

	add_extra_fields() {
		// TODO: Convert to this.dialog fields_dict
		// Swap Order: [Carrier, Customer, Transportation] to [Customer, Transportation, Carrier]. FIXME: This approach can fail miserably
		[this.mandatory[1], this.mandatory[2], this.mandatory[3]] = [this.mandatory[2], this.mandatory[3], this.mandatory[1]];

		this.mandatory.splice(3, 0, {fieldtype: "Column Break"}); // Split 'Transportation' and 'Carrier'
		this.mandatory.splice(8, 0, {fieldtype: 'Section Break', hide_border: true}); // Split 'Services' and 'Shipper'
		this.mandatory.splice(10, 0, {fieldtype: 'Column Break'}); // Split 'Shipper' and [Number of Order, Purchase Date]

		this.mandatory.splice(13, 0, {fieldtype: 'Section Break', fieldname: 'content_section', hide_border: true}, {
			fieldtype: 'Table', fieldname: 'content', options: 'Parcel Content', in_place_edit: false, fields: [
		 		{label: __('Description'), fieldtype: 'Small Text', fieldname: 'description', in_list_view: true, max_height: '4rem', columns: 6},
		 		{label: __('Tracking Number'), fieldtype: 'Data', fieldname: 'tracking_number', in_list_view: true, columns: 2},
		 		{label: __('Item Code'), fieldtype: 'Link', fieldname: 'item_code', options: 'Item', in_list_view: true, columns: 2}
		 	]}
		); // TODO: Item code with filters. Maybe we can filter if its is by the service Type?
	}

	init_post_render_dialog_operations() {
		let {tracking_number, transportation, carrier, extra_services_section, content_section, content} = this.dialog.fields_dict;

		tracking_number.df.onchange = function () {  // Override onchange to sanitize field and set carrier
			const data = cargo_management.find_carrier_by_tracking_number(this.get_input_value());

			carrier.set_input(data.carrier);      // Update the Carrier field
			this.set_input(data.tracking_number); // Tracking Number returned is sanitized
		};

		this.dialog.$wrapper.find('.modal-dialog').addClass('modal-lg'); // Making the Dialog large

		// Styling the content section
		content_section.body.css('margin-top', 0);
		content.$wrapper.find('.control-label').hide(); // Hiding Label of Content Table
		transportation.$wrapper.addClass('text-center pt-4');
		extra_services_section.wrapper.insertAfter(carrier.wrapper).removeClass('row visible-section'); // Moving entire section within a column(Done with DOM because a 'section break' will always create a new row)
	}
};
