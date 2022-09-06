frappe.provide('frappe.ui.form');

frappe.ui.form.ParcelQuickEntryForm = class ParcelQuickEntryForm extends frappe.ui.form.QuickEntryForm {

    constructor(doctype, after_insert, init_callback, doc, force) {
        super(doctype, after_insert, init_callback, doc, true)

        console.log('WORK');
    }

    set_meta_and_mandatory_fields() {
        super.set_meta_and_mandatory_fields();

        // Add onchange event to 'tracking_number' field
        // let tochange = this.mandatory.findIndex((f) => f.fieldname === 'tracking_number');

        // this.mandatory[tochange].onchange = function (e) {
        // console.log(this.dialog)
        //cargo_management.find_carrier_by_tracking_number();
        // };

        //let table_meta = frappe.get_meta('Parcel Content')
        //let table_fields = table_meta.fields;

        console.log('set_meta_and_mandatory_fields');
        //console.log(this.mandatory[10]);

        // Quick hack: form/grid.js -> add_new_row() push data to meta_fields
        //this.mandatory[10].data = null;
        //this.mandatory[10].fields = table_fields.filter(df => {
        //    if ((df.reqd || df.bold || df.allow_in_quick_entry) && !df.read_only) {

        //console.log(df);
        //return true;
        //}
        //});
    }

    // setup: function () {
    //     this.force = true;
    //     return this._super();
    // },

    // TODO: make large dialog
    render_dialog() {
        super.render_dialog();
        this.init_post_render_dialog_operations();
    }

    init_post_render_dialog_operations() {
        let {carrier: carrier_field, tracking_number: tracking_number_field} = this.dialog.fields_dict;

        tracking_number_field.df.onchange = function () {  // Override onchange to clean field and set carrier
            const data = cargo_management.find_carrier_by_tracking_number(this.get_input_value());

            this.set_input(data.tracking_number);  // Tracking Number returned is sanitized
            carrier_field.set_input(data.carrier); // Update the carrier
        };

    }

    asdget_variant_fields() {
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

}
