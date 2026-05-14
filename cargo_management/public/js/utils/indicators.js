const cargo_management = frappe.provide('cargo_management');

cargo_management.set_transportation_indicator = (
	frm, fieldname,
	child_doc_transportation = 'transportation',
	parent_doc_transportation = 'transportation'
) => {
	frm.set_indicator_formatter(fieldname, (child_doc) => {
		return child_doc[child_doc_transportation] === frm.doc[parent_doc_transportation] ? 'green' : 'red';
	});
}
