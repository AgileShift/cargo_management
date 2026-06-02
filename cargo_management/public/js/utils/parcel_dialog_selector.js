// TODO: Make this work, would work for us, on Cargo Shipment Receipt and in Warehouse Receipt
function show_selector_dialog(frm, opts) {
	// https://frappeframework.com/docs/v13/user/en/api/controls & https://frappeframework.com/docs/v13/user/en/api/dialog
	// MultiselectDialog with Parcel List -> Issue: can select multiple
	// Dialog with a Table Field of Parcel List -> Issue: can select multiple and needs a select button
	// MultiCheck Field with Parcel List as Options -> Issue: can select multiple. No extra data for parcel identification
	// Select Field with Parcel List as Options -> Issue: Small extra data for parcel identification, and need a select button or event trigger.
	// LinkSelector with Parcel List as Options -> Issue: its exactly what we need. But without search and button and configurable extra fields

	const selector_dialog = new frappe.ui.Dialog({
		title: __('Coincidences found for: {0}', [frm.doc.tracking_number]),
		static: false,          // Cannot cancel touching outside pop-up
		no_cancel_flag: false,  // Cannot cancel with keyboard
		size: 'extra-large',
		fields: [{fieldtype: 'HTML', fieldname: 'table_html'}]
	});

	selector_dialog.fields_dict.table_html.$wrapper
		.html(frappe.render_template('parcel_selector', {
			search_term: opts.search_term,
			coincidences: opts.coincidences
		}))
		.find('a').on('click', e => {
		e.preventDefault();
		selector_dialog.hide();
		frm.events.set_parcel(frm, $(e.target).attr('data-value'));
	});

	selector_dialog.show();
}
