// Copyright (c) 2020, Agile Shift and contributors
// For license information, please see license.txt

function calculate_product_total_taxes_and_import_price(frm, cdt, cdn) {
    // This func is called on Child Doctype when: product, shipping or taxes are modified.
    let row = locals[cdt][cdn]; // Getting Child Row

    row.taxes = row.has_taxes ? flt((row.product_price + row.shipping_price) * 0.07, 2) : 0.00;

    row.product_total = flt(row.product_price + row.shipping_price + row.taxes, 2);

    // We call the import price calculation to check if is by weight or percentage
    calculate_import_price(frm, cdt, cdn);
}

function calculate_import_price(frm, cdt, cdn) {
    let row = locals[cdt][cdn]; // Getting Child Row

    const minImportPrice = 5.00; // TODO: Get this dynamically

    if (row.import_price_type === 'Weight') {
        row.import_price = row.import_price_per_pound * row.weight;
    } else { // Assuming is percentage
        row.import_price = flt(row.product_total * (row.import_percentage / 100), 2)
    }

    // Setting the Minimum Price to invoice
    row.import_price = (row.import_price < minImportPrice) ? minImportPrice : row.import_price;

    frm.refresh_fields();
}


frappe.ui.form.on('Parcel Quotation', {
    onload: function (frm) {
        // Setting Currency Labels
        frm.set_currency_labels(
            ['product_price', 'shipping_price', 'taxes', 'import_price_per_pound', 'product_total', 'import_price'],
            'USD',
            'items'
        );
    },
    refresh: function(frm) {

        frm.add_custom_button(__('Render Quotation'), () => {

            $(frm.fields_dict['text'].wrapper)
                .html(frappe.render_template('parcel_quotation_details', {doc: frm.doc}));

            frappe.show_alert({message: 'Success', indicator: 'green'}, 5);
        })
    }
});

frappe.ui.form.on('Parcel Quotation Item', {
    // Children doctype of Parcel Quotation

    product_price: function (frm, cdt, cdn) {
        calculate_product_total_taxes_and_import_price(frm, cdt, cdn);
    },
    shipping_price: function (frm, cdt, cdn) {
        calculate_product_total_taxes_and_import_price(frm, cdt, cdn);
    },

    has_shipping: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn]; // Getting Child Row

        if (!row.has_shipping) {
            row.shipping_price = 0.00; // Reset. and not triggering function
        }

        calculate_product_total_taxes_and_import_price(frm, cdt, cdn);
    },

    has_taxes: function (frm, cdt, cdn) {
        calculate_product_total_taxes_and_import_price(frm, cdt, cdn);
    },


    import_price_type: function (frm, cdt, cdn) {
        calculate_import_price(frm, cdt, cdn);
    },
    weight: function(frm, cdt, cdn) {
        calculate_import_price(frm, cdt, cdn);
    },
    import_price_per_pound: function(frm, cdt, cdn) {
        calculate_import_price(frm, cdt, cdn);
    },
    import_percentage: function (frm, cdt, cdn) {
        calculate_import_price(frm, cdt, cdn);
    },

})
