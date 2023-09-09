frappe.ui.form.ControlSmallText = class ControlSmallText extends frappe.ui.form.ControlSmallText {
	// Refer to: frappe/form/controls/text.js
	make_input() {
		super.make_input();

		this.$input.css('height', '');  // Remove the inline 'height' CSS property from the input element
		this.$input.css('background', 'orange');  // Remove the inline 'height' CSS property from the input element
	}
};
