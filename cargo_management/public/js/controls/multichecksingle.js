// Override ControlMultiCheck to create a MultiCheckSingle -> See: frappe/form/controls/text.js
frappe.ui.form.ControlMultiCheckSingle = class ControlMultiCheckUnique extends frappe.ui.form.ControlMultiCheck {

	refresh_input() {
		// Override this method, We drew inspiration from: /form/controls/base_input.js -> refresh_input();
		this.set_mandatory(this.selected_options);
		this.set_required();
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
				this.selected_options = ''; // If unchecked, set to empty
			}

			// Call the on_change function with the selected option. This is useful for binding to other fields.
            this.df.on_change && this.df.on_change(this.selected_options);
        });
    }

	set_mandatory(value) {
		// Calling a core method to avoid DRY. This is necessary because MultiCheck inherits from Control rather than ControlInput(parent)
		frappe.ui.form.ControlInput.prototype.set_mandatory.call(this, value); // Refer to: /form/controls/base_input.js -> set_mandatory();
	}
	set_required() {
		this.$label.toggleClass('reqd', Boolean(this.df.reqd)); // Refer to: /form/controls/base_input.js -> set_required();
	}
};
