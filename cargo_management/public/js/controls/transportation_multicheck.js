frappe.ui.form.ControlTransportationMultiCheck = class ControlTransportationMultiCheck extends frappe.ui.form.ControlMultiCheckSingle {
	// Extends from ControlMultiCheckSingle to create a 'TransportationMultiCheck'

	parse_df_options() {
		// No need to call -> super(). See: /form/controls/multicheck.js -> parse_df_options();
		this.options = this.df.options.split('\n').map(t => ({
			value: t, description: __(t),
			label: __(t).toUpperCase() + cargo_management.icon_html(cargo_management.TRANSPORTATIONS[t].icon)
		}));
	}
}
