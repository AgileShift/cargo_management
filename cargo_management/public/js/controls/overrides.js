// Override default height on SmallText Field -> See: frappe/form/controls/text.js
frappe.ui.form.ControlSmallText = class ControlSmallText extends frappe.ui.form.ControlSmallText {
    make_input() {
        super.make_input();
        this.$input.css('height', '');  // No inline height property in all ControlSmallText
    }
};

frappe.ui.form.ControlMultiCheckUnique = class ControlMultiCheckUnique extends frappe.ui.form.ControlMultiCheck {
    make() {
        super.make();

        this.$label.toggleClass('reqd', Boolean(this.df.reqd)); // See: /form/controls/base_input.js -> set_required();
        this.$checkbox_area.css('margin-top', 'var(--margin-xs)');  // FIXME: We can set this by CSS?
    }

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
}
