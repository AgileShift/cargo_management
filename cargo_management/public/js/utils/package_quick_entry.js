frappe.provide('frappe.ui.form');

frappe.ui.form.PackageQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({

    init: function (doctype, after_insert, init_callback, doc, force) {
        this._super(doctype, after_insert, init_callback, doc, true)
    },

    set_meta_and_mandatory_fields: function () {
        this._super();

        let table_meta = frappe.get_meta('Package Content')
        let table_fields = table_meta.fields;

        console.log('set_meta_and_mandatory_fields');
        console.log(this.mandatory[10]);

        // Quick hack: form/grid.js -> add_new_row() push data to meta_fields
        this.mandatory[10].data = null;
        this.mandatory[10].fields = table_fields.filter(df => {
            if ((df.reqd || df.bold || df.allow_in_quick_entry) && !df.read_only) {

                console.log(df);
                return true;
            }
        });


    },

    // setup: function () {
    //     this.force = true;
    //     return this._super();
    // },

    // TODO: make large dialog
    render_dialog: function () {
        console.log('render_dialog');
        this._super();
        this.render_edit_in_full_page_link();
    },

    get_variant_fields: function () {
        console.log(this);

        return [
            {
                label: __("Content"),
                fieldtype: "Section Break",
                collapsible: 1
            },
            {
                fieldtype: "Table",
                fieldname: "content",
                in_place_edit: false,
                fields: [
                    {
                        label: __("Description"),
                        fieldtype: "Data",
                        fieldname: "description",
                        in_list_view: true
                    },
                    {
                        label: __("Quantity"),
                        fieldtype: "Float",
                        fieldname: "qty",
                        in_list_view: true,
                        onchange: () => {
                            console.log(this.dialog)
                        }
                    },
                    {
                        label: __("Rate"),
                        fieldtype: "Currency",
                        fieldname: "rate",
                        options: "USD",
                        in_list_view: true,
                    },
                    {
                        label: __("Amount"),
                        fieldtype: "Currency",
                        fieldname: "amount",
                        options: "USD",
                        in_list_view: true,
                        read_only: 1
                    }
                ]
            },
            {
                fieldname: "totals_section",
                fieldtype: "Section Break",
            },
            {
                fieldname: "shipping_amount",
                label: __("Shipping Amount"),
                fieldtype: "Currency",
                options: "USD",
            },
            {
                fieldtype: "Column Break"
            },
            {
                fieldname: "total",
                label: __("Total(Amt)"),
                fieldtype: "Currency",
                options: "USD"
            }
        ];

    }

});
