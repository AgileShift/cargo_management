function calculate_parcel_total(frm) {
    // Calculate the 'total' field on Parcel Doctype(Parent)
    frm.set_value('total', frm.get_sum('content', 'amount'));  // Using some built-in function: get_sum()
}

function calculate_parcel_content_amount_and_parcel_total(frm, cdt, cdn) {
    // Calculates the 'amount' field on Parcel Content Doctype(Child) and 'total' field on Parcel Doctype(Parent)
    let row = locals[cdt][cdn]; // Getting Child Row

    row.amount = row.qty * row.rate;  // Calculating amount

    refresh_field('amount', cdn, 'content'); // Show change on 'amount' field. Without triggering any event.

    calculate_parcel_total(frm); // Calculate the parent 'total' field and trigger events.
}

frappe.ui.form.on('Parcel', {

    setup: function(frm) {
        // TODO: this must be running from core frappe code. Some glitch make us hardcoded the realtime handler here.
        frappe.realtime.on('doc_update', () => { // See: https://github.com/frappe/frappe/pull/11137
            frm.reload_doc(); // Reload form UI data from db.
        });
    },

    onload: function(frm) {
        // Setting Currency Labels
        frm.set_currency_labels(['total'], 'USD');
        frm.set_currency_labels(['rate', 'amount'], 'USD', 'content');
    },

    refresh: function(frm) {
        if (frm.is_new()) {
            return;
        }

        // Better to add button here to use: 'window'. Rather than as Server Side Action Button on Doctype.
        frm.add_custom_button(__('Visit carrier detail page'), () => {
            frappe.utils.play_sound('click');  // Really Necessary?
            frappe.call({
                method: 'parcel_management.parcel_management.doctype.parcel.actions.get_carrier_detail_page_url',
                args: {carrier: frm.doc.carrier},
                callback: (r) => {  // FIXME: Don't working on mobile -> window.open(url, '_blank');
                    window.open(r.message + frm.doc.tracking_number, '_blank');
                }
            });
        });

        // Intro Message
        frappe.call({
            method: 'parcel_management.parcel_management.doctype.parcel.parcel.get_parcel_explained_status',
            args: {source_name: frm.doc.name},
            async: false, // TODO: Fix as false show deprecated message, and true renders two times the message
            callback: (r) => {
                if (r.message) { // Has a valid message
                    frm.set_intro(r.message.message, r.message.color); // frm.layout.show_message()
                }
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

    // TODO: Tracking Validator from backend, and Carrier Select helper.
});

frappe.ui.form.on('Parcel Content', {
    // Children Doctype of Parcel

    content_remove(frm) {
        calculate_parcel_total(frm);
    },

    rate: function(frm, cdt, cdn) {
        calculate_parcel_content_amount_and_parcel_total(frm, cdt, cdn);
    },

    qty: function(frm, cdt, cdn) {
        calculate_parcel_content_amount_and_parcel_total(frm, cdt, cdn);
    },

});
