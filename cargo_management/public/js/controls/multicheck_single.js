frappe.ui.form.ControlMultiCheckSingle = class ControlMultiCheckSingle extends frappe.ui.form.ControlMultiCheck {
	// Extends ControlMultiCheck to create a MultiCheckSingle see: /form/controls/multicheck.js

	refresh_input() {
		// Override this method, We drew inspiration from: /form/controls/base_input.js -> refresh_input();
		this.set_mandatory();
		this.set_required();
		this.set_bold();
	}

	bind_checkboxes() {
		// Override to enforce a single checkbox selection and return the selected option on change
		// Refer to: /form/controls/multicheck.js -> bind_checkboxes();
		$(this.wrapper).on('change', ':checkbox', (e) => {
			const $checkbox = $(e.target);

			if ($checkbox.is(':checked')) {
				this.$checkbox_area.find('input').not($checkbox).prop('checked', false); // Uncheck Others
				this.selected_options = $checkbox.attr("data-unit");
			} else {
				this.selected_options = null; // If unchecked, set to empty
			}

			if (this.df.reqd) {
				this.set_invalid(); // If required, mark or unmark field as invalid
			}

			// To pass through the selected value
			this.last_value = this.value;
			this.value = this.selected_options;

			// Call the on_change function with the selected option. This is useful for binding to other fields.
			this.df.on_change && this.df.on_change(this.selected_options);
		});
	}

	// Refer to: /form/controls/base_input.js -> set_mandatory() & set_invalid() & set_required() & set_bold()
	set_mandatory() {
		// Calling a core method to avoid DRY. This is necessary because MultiCheck inherits from Control rather than ControlInput(parent)
		frappe.ui.form.ControlInput.prototype.set_mandatory.call(this, this.selected_options);
	}
	set_invalid() {
		this.$wrapper.toggleClass("has-error", !this.selected_options);
	}
	set_required() {
		this.$label.toggleClass('reqd', Boolean(this.df.reqd));
	}
	set_bold() {
		this.$checkbox_area.toggleClass('bold', this.df.bold);
	}
};
