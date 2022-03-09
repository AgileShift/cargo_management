function calculate_package_total(frm) {
    let content_amount = frm.get_sum('content', 'amount');
    frm.doc.total = (frm.doc.has_shipping) ? content_amount + frm.doc.shipping_amount : content_amount;  // Calculate the 'total' field on Package Doctype(Parent)

    frm.refresh_fields(); // FIXME: Maybe is not the better way..
}

function calculate_package_content_amount_and_package_total(frm, cdt, cdn) {
    // Calculates the 'amount' field on Package Content Doctype(Child) and 'total' field on Package Doctype(Parent)
    let content_row = locals[cdt][cdn]; // Getting Child Row

    content_row.amount = content_row.qty * content_row.rate;  // Calculating amount in eddited row

    calculate_package_total(frm); // Calculate the parent 'total' field and trigger refresh event
}

// todo: MATCH the new and current fields! import_price for example
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
        frm.set_currency_labels(['rate', 'amount'], 'USD', 'content');
    },

    refresh: function(frm) {
        if (frm.is_new()) {
            return;
        }

        frm.add_custom_button(__('Visit carrier detail page'), () => frm.events.visit_carrier_detail_page(frm.doc));

        if (frm.doc.assisted_purchase) { // If is Assisted Purchase will have related Sales Order and Sales Order Item.
            frm.add_custom_button(__('Sales Order'), () => frm.events.sales_order_dialog(frm) , __('Get Items From'));
        }

        frm.events.get_detailed_status_message(frm); // Intro Message
    },

    tracking_number: function (frm) {
        frm.doc.tracking_number = frm.doc.tracking_number.trim().toUpperCase();  // Sanitize field

        if (!frm.doc.tracking_number) {
            return;
        }

        frappe.call({
            method: 'cargo_management.package_management.doctype.package.actions.find_carrier_by_tracking_number',
            type: 'GET',
            freeze: true,
            freeze_message: __('Searching Carrier...'),
            args: {tracking_number: frm.doc.tracking_number},
            callback: (r) => {
                frm.doc.carrier = r.message.carrier;
                refresh_field(['carrier', 'tracking_number']);

                frappe.show_alert('Carrier: ' + r.message.carrier);  // TODO: Delete this comment?
            }
        });
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

    // Custom Functions

    visit_carrier_detail_page: function (doc) {
        frappe.call({
            method: 'cargo_management.package_management.doctype.package.actions.get_carrier_detail_page_url',
            type: 'GET',
            args: {carrier: doc.carrier},
            freeze: true,
            freeze_message: __('Opening carrier detail page...'),
            callback: (r) => {
                window.open(r.message + doc.tracking_number, '_blank');
            }
        });
    },

    get_detailed_status_message: function (frm) {
        frappe.call({
            method: 'cargo_management.package_management.doctype.package.actions.get_explained_status',
            type: 'GET',
            args: {source_name: frm.doc.name},
            callback: (r) => {
                if ($.isArray(r.message.message)) { // If there are multiple messages.
                    r.message.message = r.message.message.map(message => '<div>' + message + '</div>').join('');
                }

                frm.set_intro(r.message.message, ''); // FIXME: Core only allows blue & yellow: layout.js -> show_message()
                frm.layout.message.removeClass().addClass('form-message ' + r.message.color); // Set same color on message as on status indicator dot.
            }
        });
    },

    //https://github.com/frappe/frappe/pull/12471 and https://github.com/frappe/frappe/pull/14181/files
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
                frm.events.so_items_dialog(frm, selections);
            }
        });
    },

    so_items_dialog: async function (frm, sales_orders) {
        // Getting all sales order items from Sales Order
        let sale_order_items = await frappe.db.get_list('Sales Order Item', {
            filters: {'parent': ['in', sales_orders]},
            fields: ['name as docname', 'item_code', 'description', 'qty', 'rate']
        });

        const so_items_dialog = new frappe.ui.form.MultiSelectDialog({
            doctype: 'Sales Order Item',
            target: frm,
            setters: {
                // item_code: undefined,
                // qty: undefined,
                // rate: undefined
            },
            data_fields: [
                {
                    fieldtype: 'Currency',
                    options: "USD",
                    fieldname: "rate",
                    read_only: 1,
                    hidden: 1,
                },
                {
                    fieldname: 'item_code',
                    fieldtype: 'Data',
                    label: __('Item sshhshsh')
                }],
            get_query: () => {
                return {
                    filters: {
                        parent: ['in', sales_orders]
                    }
                }
            },
            add_filters_group: 1,
            action: (jkjk) => {
                console.log(jkjk);
            },
            primary_action_label: __('Select')
        });

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
