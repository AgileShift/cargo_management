function calculate_package_total(frm) {
    let content_amount = frm.get_sum('content', 'amount');  // Using some built-in function: get_sum()
    frm.doc.total = (frm.doc.has_shipping) ? content_amount + frm.doc.shipping_amount : content_amount;  // Calculate the 'total' field on Package Doctype(Parent)

    frm.refresh_fields();  // Refresh all fields. FIXME: Maybe is not the better way..
}

function calculate_package_content_amount_and_package_total(frm, cdt, cdn) {
    // Calculates the 'amount' field on Package Content Doctype(Child) and 'total' field on Package Doctype(Parent)
    let content_row = locals[cdt][cdn]; // Getting Child Row

    content_row.amount = content_row.qty * content_row.rate;  // Calculating amount in eddited row

    calculate_package_total(frm); // Calculate the parent 'total' field and trigger events.
}

// todo: MATCH the new and current fields! import_price for example
// TODO: Tracking Validator from backend and Carrier Select helper.
// TODO: Finish The Progress Bar -> frm.dashboard.add_progress("Status", []

frappe.ui.form.on('Package', {

    onload: function(frm) {
        // Setting custom queries
        frm.set_query('item_code', 'content', () => {
            return {
                filters: {
                    'is_sales_item': true,
                    'has_variants': false
                }
            }
        });

        // Setting Currency Labels
        frm.set_currency_labels(['total', 'shipping_amount'], 'USD');
        // frm.set_currency_labels(['rate', 'amount'], 'USD', 'content');
    },

    refresh: function(frm) {
        if (frm.is_new()) {
            return;
        }

        frm.events.get_detailed_status_message(frm); // Intro Message

        if (frm.doc.assisted_purchase) { // If is Assisted Purchase will have related Sales Order and Sales Order Item.
            frm.add_custom_button(__('Sales Order'), () => frm.events.sales_order_dialog(frm) , __('Get Items From'));
        }
        frm.add_custom_button(__('Visit carrier detail page'), () => frm.events.visit_carrier_detail_page(frm.doc));
    },

    has_shipping: function (frm) {
        if (!frm.doc.has_shipping) {
            frm.doc.shipping_amount = 0; // Empty the value of the field.
        }
        calculate_package_total(frm);
    },

    shipping_amount: function (frm) {
        calculate_package_total(frm);
    },

    get_detailed_status_message: function (frm) {
        frappe.call('cargo_management.package_management.doctype.package.actions.get_explained_status', {
            source_name: frm.doc.name
        }).then(r => {
            if ($.isArray(r.message.message)) { // If there are multiple messages.
                r.message.message = r.message.message.map(message => '<div>' + message + '</div>').join('');
            }

            frm.set_intro(r.message.message, ''); // FIXME: Core only allows blue & yellow: layout.js -> show_message()
            frm.layout.message.removeClass().addClass('form-message ' + r.message.color); // Set same color on message as on status indicator dot.
        });
    },

    visit_carrier_detail_page: function (doc) {
        frappe.call({
            method: 'cargo_management.package_management.doctype.package.actions.get_carrier_detail_page_url',
            args: {carrier: doc.carrier},
            freeze: true,
            freeze_message: __('Opening detail page...'),
            callback: (r) => {
                window.open(r.message + doc.tracking_number, '_blank');
            }
        });
    },

    sales_order_dialog: function (frm) {
        const so_dialog = new frappe.ui.form.MultiSelectDialog({
            doctype: 'Sales Order',
            target: frm,
            setters: {
                delivery_date: undefined,
                status: undefined
            },
            add_filters_group: 1,
            get_query: () => {
                return {
                    filters: {  // TODO: Only uncompleted orders!
                        docstatus: 1,
                        customer: frm.doc.customer,
                    }
                };
            },
            action: (selections) => {
                if (selections.length === 0) {
                    frappe.msgprint(__("Please select {0}", [so_dialog.doctype]))
                    return;
                }
                // so_dialog.dialog.hide();
                frm.events.so_items_dialog(selections);
            }
        });
    },

    so_items_dialog: async function (sales_orders) {
        // Getting all sales order items from Sales Order
        let sale_order_items = await frappe.db.get_list('Sales Order Item', {
            filters: {'parent': ['in', sales_orders]},
            fields: ['name as docname', 'item_code', 'description', 'qty', 'rate']
        });

        const so_items_dialog = new frappe.ui.Dialog({ // FIXME: Make MultiSelectDialog?
            title: __('Select Items'),
            fields: [
                {
                    fieldname: 'trans_items',
                    fieldtype: 'Table',
                    label: __('Items'),
                    cannot_add_rows: true,
                    in_place_edit: true,
                    reqd: 1,
                    data: sale_order_items,
                    fields: [
                        {
                            fieldtype: 'Data',
                            fieldname: "docname",
                            read_only: 1,
                            hidden: 1,
                        }, {
                            fieldtype: 'Link',
                            fieldname: "item_code",
                            options: 'Item',
                            in_list_view: 1,
                            read_only: 1,
                            label: __('Item Code')
                        }, {
                            fieldtype: 'Data',
                            fieldname: "description",
                            in_list_view: 1,
                            read_only: 1,
                            label: __('Description')
                        }, {
                            fieldtype: 'Float',
                            fieldname: "qty",
                            read_only: 1,
                            in_list_view: 1,
                            label: __('Qty'),
                            // precision: get_precision("qty")
                        }, {
                            fieldtype: 'Currency',
                            fieldname: "rate",
                            options: "currency",
                            read_only: 1,
                            in_list_view: 1,
                            label: __('Rate'),
                            // precision: get_precision("rate")
                        }
                    ]
                },
            ],
            primary_action: function (jkjk) {
                console.log(jkjk);
            },
            primary_action_label: __('Select')
        });

        so_items_dialog.fields_dict.trans_items.grid.refresh();
        so_items_dialog.show();
    }
});

// Children Doctype of Package
frappe.ui.form.on('Package Content', {
    content_remove(frm) {
        calculate_package_total(frm);
    },

    rate: function(frm, cdt, cdn) {
        calculate_package_content_amount_and_package_total(frm, cdt, cdn);
    },

    qty: function(frm, cdt, cdn) {
        calculate_package_content_amount_and_package_total(frm, cdt, cdn);
    }
});
//192