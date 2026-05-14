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
}
