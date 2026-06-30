const cargo_management = frappe.provide('cargo_management');

cargo_management.set_transportation_indicator = (
	frm, fieldname,
	child_doc_transportation = 'transportation',
	parent_doc_transportation = 'transportation'
) => {
	// TODO: Complete, this if the a child table, when the row gets rendered!
	// mega distinct of the get_indicator, for the list view(status) field.

	frm.set_indicator_formatter(fieldname, (child_doc) => {
		return child_doc[child_doc_transportation] === frm.doc[parent_doc_transportation] ? 'green' : 'red';
	});
};

cargo_management.clear_form_transportation_indicator = (frm) => {
	frm.page.indicator.parent().find('.transportation-indicator').remove();
};

cargo_management.render_form_transportation_indicator = (frm, transportation = frm.doc.transportation) => {
	cargo_management.clear_form_transportation_indicator(frm);

	if (!transportation || !cargo_management.TRANSPORTATIONS[transportation]) {
		return;
	}

	frm.page.indicator.parent().append(cargo_management.transportation_indicator(transportation));
};

cargo_management.setup_form_transportation_indicator = (frm) => {
	$(frm.wrapper)
		.off('dirty.form_transportation_indicator')
		.on('dirty.form_transportation_indicator', () => {
			cargo_management.clear_form_transportation_indicator(frm);
		});
};
