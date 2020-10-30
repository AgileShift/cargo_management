function calculate_product_total_taxes_and_import_price(frm, cdt, cdn) {
    // This func is called on Child Doctype when: product, shipping or taxes are modified.
    let row = locals[cdt][cdn]; // Getting Child Row

    row.shipping_price = row.has_shipping ? row.shipping_price : 0.00;
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
        // TODO: Validate the doctype and call save inside here. Se we leverage the validation to frappe

        frm.add_custom_button(__('Render Quotation'), () => {
            const date_string_options = {day: 'numeric', month: 'long', timeZone: 'utc'}; // Settings

            let parsed_items = frm.doc.items.map(item => {
                let item_to_parse = Object.assign({}, item); // We Copy the item

                item_to_parse.closest_arrival_date = new Date(item.closest_arrival_date).toLocaleDateString('es-ES', date_string_options);
                item_to_parse.longest_arrival_date = (item.longest_arrival_date) ? new Date(item.longest_arrival_date).toLocaleDateString('es-ES', date_string_options) : null;

                if (item.closest_departure_date) { // If has a closest departure date calculate closest delivery date.
                    item_to_parse.closest_delivery_date = new Date(
                        moment(item.closest_departure_date).add(frm.doc.transit_days, 'days') // FIXME: frappe.datetime.add_days('', '')
                    ).toLocaleDateString('es-ES', date_string_options);
                }
                if (item.longest_departure_date) {
                    item_to_parse.longest_delivery_date = new Date(
                        moment(item.longest_departure_date).add(frm.doc.transit_days, 'days')
                    ).toLocaleDateString('es-ES', date_string_options);
                }

                return item_to_parse
            });

            let doc_to_render = Object.assign({}, frm.doc, {items: parsed_items}); // We change the doc to make date human readable.

            $(frm.fields_dict['text'].wrapper)
                .html(frappe.render_template('parcel_quotation_details', {doc: doc_to_render}));

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
