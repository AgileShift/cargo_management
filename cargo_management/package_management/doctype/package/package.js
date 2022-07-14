function calculate_package_total(frm) {
    frm.doc.total = frm.get_sum('content', 'amount') + frm.doc.shipping_amount;  // Calculate the 'total' field on Package Doctype(Parent)

    frm.refresh_field('total');
}

function calculate_package_content_amount_and_package_total(frm, cdt, cdn) {
    // Calculates the 'amount' field on Package Content Doctype(Child) and 'total' field on Package Doctype(Parent)
    let content_row = locals[cdt][cdn]; // Getting Child Row

    content_row.amount = content_row.qty * content_row.rate;  // Calculating amount in edited row

    refresh_field('amount', cdn, 'content');
    calculate_package_total(frm); // Calculate the parent 'total' field and trigger refresh event
}

frappe.ui.form.on('Package', {

    setup: function (frm) {
        $('.layout-side-section').hide(); // Little Trick to work better FIXME use frm.page.layout
    },

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

        // Add Icon to the Page Indicator
        frm.page.indicator.children().append(cargo_management.transportation_icon_html(frm.doc.transportation));

        // TODO: Make a Progress Bar -> frm.dashboard.add_progress("Status", []
        frm.events.build_custom_buttons(frm);  // Adding Custom buttons
        frm.events.show_explained_status(frm); // Intro Message
    },

    tracking_number: function (frm) {
        frm.doc.tracking_number = frm.doc.tracking_number.trim().toUpperCase();  // Sanitize field

        if (!frm.doc.tracking_number) {
            return;
        }

        const data = cargo_management.find_carrier_by_tracking_number(frm.doc.tracking_number);

        frm.doc.carrier = data.carrier;
        refresh_many(['tracking_number', 'carrier']);
    },

    shipping_amount: function (frm) {
        calculate_package_total(frm);
    },

    // Custom Functions

    show_explained_status: function (frm) {
        frappe.call({
            method: 'cargo_management.package_management.doctype.package.actions.get_explained_status',
            type: 'GET', args: {source_name: frm.doc.name},
            callback: (r) => {
                r.message.message.forEach(m => frm.layout.show_message(m, ''))  // FIXME: Core overrides color
                frm.layout.message.removeClass().addClass('form-message ' + r.message.color);
            }
        });
    },

    build_custom_buttons: function (frm) {
        cargo_management.load_carrier_settings(frm.doc.carrier).then((settings) => {
            if (settings.api)  // TODO: easypost_id or other APIs?
                frm.add_custom_button(__('Get Updates from Carrier'), () => frm.events.get_data_from_api(frm));

            settings.urls.forEach(url => frm.add_custom_button(url.title, () => window.open(url.url + frm.doc.tracking_number)));
        });

        if (frm.doc.assisted_purchase) { // If is Assisted Purchase will have related Sales Order and Sales Order Item.
            frm.add_custom_button(__('Sales Order'), () => frm.events.sales_order_dialog(frm), __('Get Items From'));
        }
    },

    get_data_from_api: function (frm) {
        // WORK ON THIS. We have to delete some data
        frappe.call({
            method: 'cargo_management.package_management.doctype.package.actions.get_data_from_api',
            freeze: true, freeze_message: __('Updating from Carrier...'), args: {source_name: frm.doc.name},
            callback: (r) => {
                frappe.model.sync(r.message);
                frm.refresh();
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
