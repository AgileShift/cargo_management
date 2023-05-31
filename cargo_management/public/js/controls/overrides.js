frappe.ui.form.ControlSmallText = class ControlSmallText extends frappe.ui.form.ControlSmallText {
    // Refer to: frappe/form/controls/text.js
    make_input() {
        super.make_input();
        this.$input.css('height', '');  // Remove the inline 'height' CSS property from the input element
    }
};

frappe.ui.form.ControlMultiCheck = class ControlMultiCheck extends frappe.ui.form.ControlMultiCheck {
	// Override the refresh() method in ControlMultiCheck to avoid extra calls to refresh_input()
	// For more details, refer to: /form/controls/multicheck.js and its parent: /form/controls/base_control.js
	refresh() {
		this.set_options();     // As Parent
		this.bind_checkboxes(); // As Parent
		frappe.ui.form.Control.prototype.refresh.call(this); // bypasses the extra calls to refresh_input(). It's equivalent to calling super.super.
	}
};
