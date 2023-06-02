frappe.provide('frappe.ui.form');

frappe.ui.form.ParcelQuickEntryForm = class ParcelQuickEntryForm extends frappe.ui.form.QuickEntryForm {
	constructor(doctype, after_insert, init_callback, doc, force) {
		super(doctype, after_insert, init_callback, doc, force);
	}

	render_dialog() {
		this.add_extra_fields(); // Adding Table Field after executing is_quick_entry()
		super.render_dialog();
		this.init_post_render_dialog_operations(); // Custom method to modify DOM properties after the dialog has been rendered
	}

	init_post_render_dialog_operations() {
		let {carrier, tracking_number, extra_services_section, content_section, content, transportation_options} = this.dialog.fields_dict;

		tracking_number.df.onchange = function () {  // Override onchange to sanitize field and set carrier
			const data = cargo_management.find_carrier_by_tracking_number(this.get_input_value());

			this.set_input(data.tracking_number);  // Tracking Number returned is sanitized
			carrier.set_input(data.carrier);       // Update the carrier field
		};

		this.dialog.$wrapper.find('.modal-dialog').addClass('modal-lg'); // Making the Dialog large
		extra_services_section.wrapper.insertAfter(carrier.wrapper).removeClass('row visible-section'); // Moving an entire section within a column

		// Styling the content section
		transportation_options.$wrapper.addClass('text-center');
		content_section.wrapper.css({'padding-top': 0, 'border': 'none'});
		content_section.body.css('margin-top', 0);
		content.$wrapper.find('.control-label').hide(); // Hiding Label of Content Table
	}

	add_extra_fields() {
		// FIXME: This approach can fail miserably and is not recommended
		[this.mandatory[1], this.mandatory[2]] = [this.mandatory[2], this.mandatory[1]]; // Swap Order: Customer with Carrier

		// Insert New Fields in between Customer and Carrier. FIXME: better options?
		this.mandatory.splice(2, 0,{
			fieldtype: 'MultiCheckSingle', fieldname: 'transportation_options', label: __('Transportation'), reqd: true, bold: true, columns: 2,
			options: ['Sea', 'Air'].map(t => ({value: t, description: __(t), label: __(t).toUpperCase() + cargo_management.icon_html(cargo_management.transportations[t].icon)})),
			on_change: (selected) => this.doc.transportation = selected // Bind the selected checkbox with the doc field
		}, {fieldtype: "Column Break"});

		this.mandatory.push(
			{fieldtype: 'Section Break', fieldname: 'content_section'},
			{fieldtype: 'Table', fieldname: 'content', options: 'Parcel Content', in_place_edit: false, fields: [
				{label: __('Description'), fieldtype: 'Small Text', fieldname: 'description', in_list_view: true},
				{label: __('Item Code'), fieldtype: 'Link', fieldname: 'item_code', options: 'Item', in_list_view: true}
			]}
		); // TODO: Item code with filters. Maybe we can filter if its is by the service Type?
	}
};
