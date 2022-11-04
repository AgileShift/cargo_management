frappe.ui.form.on("Quotation", {

    refresh: function (frm) {
        frm.add_custom_button(__('Add Item'), () => frm.events.add_item_dialog(frm));
    },

    calculate_item_total: function (dialog) {
        let {price, qty, subtotal, taxes, shipping, total, has_taxes, shipping_taxes} = dialog.fields_dict;

        subtotal.value = price.value * qty.value;

        taxes.value = (has_taxes.value) ? subtotal.value * 0.07 : 0;
        taxes.value += (shipping_taxes.value) ? shipping.value * 0.07 : 0;

        total.value = subtotal.value + taxes.value + shipping.value;

        dialog.refresh();
    },

    add_item_dialog: function (frm) {
        let dialog = new frappe.ui.Dialog({
            title: __('Add Details'),
            fields: [
                {
                    label: 'URL or Name',
                    fieldname: 'link',
                    fieldtype: 'Data'
                },
                {
                    fieldtype: 'Section Break',
                    hide_border: 1
                },
                {
                    label: 'Description',
                    fieldname: 'description',
                    fieldtype: 'Small Text'
                },
                {
                    fieldtype: 'Section Break'
                },

                {
                    label: 'Price',
                    fieldname: 'price',
                    fieldtype: 'Currency',
                    options: 'USD',
                    onchange: () => frm.events.calculate_item_total(dialog)
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Quantity',
                    fieldname: 'qty',
                    fieldtype: 'Int',
                    default: 1,
                    onchange: () => frm.events.calculate_item_total(dialog)
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Subtotal',
                    fieldname: 'subtotal',
                    fieldtype: 'Currency',
                    options: 'USD',
                    read_only: true
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Taxes',
                    fieldname: 'taxes',
                    fieldtype: 'Currency',
                    options: 'USD',
                    read_only: true
                },
                {
                    label: 'Has Taxes',
                    fieldname: 'has_taxes',
                    fieldtype: 'Check',
                    default: true,
                    onchange: () => frm.events.calculate_item_total(dialog)
                },

                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Shipping',
                    fieldname: 'shipping',
                    fieldtype: 'Currency',
                    options: 'USD',
                    onchange: () => frm.events.calculate_item_total(dialog)
                },
                {
                    label: 'Shipping Taxes',
                    fieldname: 'shipping_taxes',
                    fieldtype: 'Check',
                    onchange: () => frm.events.calculate_item_total(dialog)
                },

                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Total',
                    fieldname: 'total',
                    fieldtype: 'Currency',
                    options: 'USD',
                    read_only: true
                },

                {
                    fieldtype: 'Section Break'
                },
                {
                    label: 'Closest Arrival Date',
                    fieldname: 'arrival_date_1',
                    fieldtype: 'Date'
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Longest Arrival Date',
                    fieldname: 'arrival_date_2',
                    fieldtype: 'Date'
                },
                {
                    fieldtype: 'Section Break'
                },
                {
                    label: 'Aprox Weight (LB)',
                    fieldname: 'weight',
                    fieldtype: 'Float'
                },
                {
                    fieldtype: 'Section Break'
                },
                {
                    label: 'AIR',
                    fieldname: 'sea_quote',
                    fieldtype: 'Check',
                    default: true
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'SEA',
                    fieldname: 'air_quote',
                    fieldtype: 'Check',
                    default: true
                },
            ],
            primary_action_label: 'Add To Quote',
            primary_action(values) {
                dialog.hide();

                frm.add_child('items', {
                    'item_name': values.link,
                    'description': values.description,
                    'qty': values.qty,
                    'rate': values.total,
                    'closest_arrival_date': values.closest_arrival_date,
                    'longest_arrival_date': values.longest_arrival_date
                });

                frm.refresh_field('items')
            }
        });

        dialog.show()
    }
});
