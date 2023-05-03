frappe.provide('frappe.ui.form');

frappe.ui.form.ParcelQuickEntryForm = class ParcelQuickEntryForm extends frappe.ui.form.QuickEntryForm {
	constructor(doctype, after_insert, init_callback, doc, force) {
		super(doctype, after_insert, init_callback, doc, force);
	}

	set_meta_and_mandatory_fields() {
		super.set_meta_and_mandatory_fields();

		// FIXME: Changes fields before calling render_dialog(); This approach can fail miserably and is not recommended
		[this.mandatory[1], this.mandatory[2], this.mandatory[3]] = [this.mandatory[2],  this.mandatory[3], this.mandatory[1]]; // Swap Order
		this.mandatory.splice(3, 0, {fieldtype: "Column Break"}); // Insert new field on custom index
	}

	render_dialog() {
		this.mandatory.push(...this.get_extra_fields());  // Adding a Table Field after executing is_quick_entry()
		super.render_dialog();
		this.init_post_render_dialog_operations(); // Custom function to modify DOM properties after the dialog has been rendered
	}

	init_post_render_dialog_operations() {
		let {carrier, tracking_number, extra_services_section, content_section, content} = this.dialog.fields_dict;

		tracking_number.df.onchange = function () {  // Override onchange to sanitize field and set carrier
			const data = cargo_management.find_carrier_by_tracking_number(this.get_input_value());

			this.set_input(data.tracking_number);  // Tracking Number returned is sanitized
			carrier.set_input(data.carrier);       // Update the carrier field
		};

		this.dialog.$wrapper.find('.modal-dialog').addClass('modal-lg'); // Making the Dialog large
		extra_services_section.wrapper.insertAfter(carrier.parent).removeClass('row visible-section'); // Moving an entire section within a column

		// Styling the content section
		content_section.wrapper.css({'padding-top': 0, 'border': 'none'});
		content_section.body.css('margin-top', 0);
		content.$wrapper.find('.control-label').hide(); // Hiding Label of Content Table
	}

	get_extra_fields() {
		// TODO: // Item code with filters. Maybe we can filter if its is by the service Type?
		return [
			{fieldtype: 'Section Break', fieldname: 'content_section'},
			{fieldtype: 'Table', fieldname: 'content', options: 'Parcel Content', in_place_edit: false, fields: [
				{label: __('Description'), fieldtype: 'Data', fieldname: 'description', in_list_view: true},
				{label: __('Item Code'), fieldtype: 'Link', fieldname: 'item_code', options: 'Item', in_list_view: true}]}
		];
	}
}
