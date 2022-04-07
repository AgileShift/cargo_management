frappe.provide('frappe.ui.form');

frappe.ui.form.ControlSmallText = frappe.ui.form.ControlSmallText.extend({
    make_input: function () {
        this._super();
        this.$input.css('height', '');  // No inline height property in all ControlSmallText -> See: frappe/form/controls/text.js
    }
});

frappe.ui.form.ControlMultiCheckUnique = frappe.ui.form.ControlMultiCheck.extend({
    make() {
        this._super();

        this.$label.toggleClass('reqd', Boolean(this.df.reqd)); // See: /form/controls/base_input.js -> set_required();
        this.$checkbox_area.css('margin-top', 'var(--margin-xs)');  // FIXME: We can set this by CSS?
    },

    bind_checkboxes() {
        // We Override this def to be able to make Check Unique and return the selected option on change
        // See: /form/controls/multicheck.js -> bind_checkboxes();
        $(this.wrapper).on('change', ':checkbox', e => {
            const $checkbox = $(e.target);
            let option_name = '';

            if ($checkbox.is(':checked')) {
                this.$checkbox_area.find('input').not($checkbox).prop('checked', false); // Uncheck Others
                option_name = $checkbox.attr("data-unit");
            }

            this.df.on_change && this.df.on_change(option_name);
        });
    }
});
