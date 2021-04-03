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

// todo: MATCH the new and current fields!! import_price for example

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

        // Better to add button here to use: 'window'. Rather than as Server Side Action Button on Doctype.
        frm.add_custom_button(__('Visit carrier detail page'), () => {
            //frappe.utils.play_sound('click');  // Really Necessary?. FIXME: On Safari plays after window is closed!
            frappe.call({
                method: 'cargo_management.package_management.doctype.package.actions.get_carrier_detail_page_url',
                args: {carrier: frm.doc.carrier},
                freeze: true,
                freeze_message: __('Opening detail page...'),
                // async: false, // FIXME: allow window to open a new tab in safari, also it seems to delay play_sound
                callback: (r) => {
                    window.open(r.message + frm.doc.tracking_number, '_blank');
                }
            });
        });

        // Intro Message
        frappe.call({
            method: 'cargo_management.package_management.doctype.package.package.get_package_explained_status',
            args: {source_name: frm.doc.name},
            // async: false, // TODO: Fix as false show deprecated message, and true renders two times the message
            callback: (r) => {
                let intro_message = '';

                if (Array.isArray(r.message.message)) { // If there are multiple messages.
                    r.message.message.forEach((message) => {
                        intro_message += "<div>" + message + "</div>";
                    });
                }

                frm.set_intro(intro_message ? intro_message : r.message.message, r.message.color);  // frm.layout.show_message()

                // FIXME: Override default color layout set in core: layout.js -> show_message def, core only allows blue and yellow
                frm.layout.message.removeClass(frm.layout.message_color).addClass(r.message.color); // This allow to have same color on indicator, dot and alert..
            }
        });

        // TODO: Finish The Progress Bar
        // frm.dashboard.add_progress("Status", [
        //     {
        //         title: "Not sent" + " Queued",
        //         width: "25%",
        //         progress_class: "progress-bar-info"
        //     },
        //     {
        //         title: "Sent" + " Sent",
        //         width: "10%",
        //         progress_class: "progress-bar-success"
        //     },
        //     {
        //         title: "Sending" + " Sending",
        //         width: "5%",
        //         progress_class: "progress-bar-warning"
        //     },
        //     {
        //         title: "Error" + "% Error",
        //         width: "60%",
        //         progress_class: "progress-bar-danger"
        //     }
        // ]);
    },

    has_shipping: function (frm) {
        if (!frm.doc.has_shipping) {
            frm.doc.shipping_amount = 0; // Empty the value of the field.
        }
        calculate_package_total(frm);
    },

    shipping_amount: function (frm) {
        calculate_package_total(frm);
    }

    // TODO: Tracking Validator from backend and Carrier Select helper.
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
    },
});
