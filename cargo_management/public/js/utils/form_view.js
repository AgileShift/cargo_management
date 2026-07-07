const cargo_management = frappe.provide('cargo_management');

cargo_management.form_view = {
	set_child_transportation_indicator_formatter(frm, fieldname, child_doc_transportation = 'transportation', parent_doc_transportation = 'transportation') {
		// TODO: Complete, this if the a child table, when the row gets rendered!

		frm.set_indicator_formatter(fieldname, (child_doc) => {
			return child_doc[child_doc_transportation] === frm.doc[parent_doc_transportation] ? 'green' : 'red';
		});
	},

	format_transportation_indicator(transportation) {
		if (!transportation || !cargo_management.TRANSPORTATIONS[transportation]) {
			return '';
		}

		const opts = cargo_management.TRANSPORTATIONS[transportation];

		return `<span class="indicator-pill no-indicator-dot whitespace-nowrap ${opts.color} transportation-indicator" style="margin-left: 10px">
			<span>${__(transportation)}${cargo_management.icon_html(opts.icon)}</span>
		</span>`; // See more of this on ui/page.js -> set_indicator() and clear_indicator()
	},

	clear_transportation_indicator(frm) {
		frm.page.indicator.parent().find('.transportation-indicator').remove();
	},

	render_transportation_indicator(frm, transportation = frm.doc.transportation) {
		cargo_management.form_view.clear_transportation_indicator(frm);

		if (!transportation || !cargo_management.TRANSPORTATIONS[transportation]) {
			return;
		}

		frm.page.indicator.parent().append(cargo_management.form_view.format_transportation_indicator(transportation));
	},

	setup_transportation_indicator(frm) {
		$(frm.wrapper)
			.off('dirty.form_transportation_indicator')
			.on('dirty.form_transportation_indicator', () => {
				cargo_management.form_view.clear_transportation_indicator(frm);
			});
	}
};
