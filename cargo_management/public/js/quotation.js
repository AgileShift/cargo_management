frappe.ui.form.on("Quotation", {

    refresh: function (frm) {
        frappe.db.get_doc('Parcel Selling Settings').then(r => {
            // TODO: Change only if is not set!
            frm.doc.transit_days_sea = r.transit_days_sea_1;
            frm.doc.transit_days_sea_2 = r.transit_days_sea_2;
            frm.doc.transit_days_air = r.transit_days_air_1;
            frm.doc.transit_days_air_2 = r.transit_days_air_2;
        });

        frm.add_custom_button(__('Add Item'), () => frm.events.add_item_dialog(frm));

        // frm.set_df_property('naming_series', 'hidden', true);
        frm.set_df_property('quotation_to', 'hidden', true);
        // frm.set_df_property('party_name', 'reqd', false);
        // frm.set_df_property('customer_name', 'read_only', false);
        frm.set_df_property('scan_barcode', 'hidden', true);
        frm.set_df_property('taxes_and_charges', 'hidden', true);
        frm.set_df_property('tax_category', 'hidden', true);
    },

    calculate_item_total: function (dialog) {
        let {price, qty, subtotal, taxes, shipping_cost, total, has_taxes, shipping_taxes} = dialog.fields_dict;

        subtotal.value = price.value * qty.value;

        taxes.value = (has_taxes.value) ? subtotal.value * 0.07 : 0;
        taxes.value += (shipping_taxes.value) ? shipping_cost.value * 0.07 : 0;

        total.value = subtotal.value + taxes.value + shipping_cost.value;

        dialog.refresh();
    },

    add_item_dialog: function (frm) {
        let dialog = new frappe.ui.Dialog({
            title: __('Add Item'),
            fields: [
                {
                    label: 'Item Code',
                    fieldname: 'item_code',
                    fieldtype: 'Link',
                    options: 'Item',
                    reqd: 1
                },
                {
                    label: 'Item Name',
                    fieldname: 'item_name',
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
                    reqd: 1,
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
                    reqd: 1,
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
                    fieldname: 'shipping_cost',
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
                    label: 'Weight',
                    fieldname: 'by_weight',
                    fieldtype: 'Check',
                    default: true
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Margin',
                    fieldname: 'by_margin',
                    fieldtype: 'Check'
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Fixed',
                    fieldname: 'fixed',
                    fieldtype: 'Check'
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
                }
            ],
            primary_action_label: __('Add To Quote'),
            primary_action(values) {
                dialog.hide();

                frm.add_child('items', {
                    'uom': 'Unit',  // FIXME: fetch_from -> stock_uom ?

                    'item_code': values.item_code,
                    'item_name': values.item_name,
                    'description': values.description,
                    'qty': values.qty,
                    'rate': values.total,
                    'has_taxes': values.has_taxes,
                    'shipping_cost': values.shipping_cost,
                    'closest_arrival_date': values.arrival_date_1,
                    'longest_arrival_date': values.arrival_date_2
                });

                frm.fields_dict['quote_in_text'].$wrapper.html(`
                    <a>{ROPA}</a>
                `)

                frm.refresh_field('items');
            }
        });

        dialog.show()
    }
});
