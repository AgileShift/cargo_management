function calculate_parcel_total(frm) {
    // Calculate the 'total' field on Parcel Doctype(Parent)
    frm.doc.total = frm.get_sum('content', 'amount');  // Using some built-in function: get_sum()
    frm.refresh_field('total');  // Using frm here to refresh the parent field 'total'.
}

function calculate_parcel_content_amount_and_parcel_total(frm, cdt, cdn) {
    // Calculates the 'amount' field on Parcel Content Doctype(Child) and 'total' field on Parcel Doctype(Parent)
    let parcel_content_row = locals[cdt][cdn]; // Getting Child Row

    parcel_content_row.amount = parcel_content_row.qty * parcel_content_row.rate;  // Calculating amount

    refresh_field('amount', cdn, 'content'); // Show change on 'amount' field. Without triggering any event.

    calculate_parcel_total(frm); // Calculate the parent 'total' field and trigger events.
}

frappe.ui.form.on('Parcel', {

    setup: function(frm) {
        // This allow us to send non-obtrusive messages from the backend: FIXME: is another way? Refactor.
        // https://frappeframework.com/docs/user/en/api/dialog#frappeshow_alert its not available for Python API.
        frappe.realtime.on('display_alert', function (msg) {
            frappe.show_alert({message: msg, indicator: 'yellow'}, 5);
        }); // TODO: Validate this action when the list page is open!

        // This is for python api alert on new data received.
        frappe.realtime.on('new_carrier_data', () => {
            frm.reload_doc(); // Reload form UI data from db.
        });
    },

    onload: function(frm) {
        // Setting Currency Labels
        frm.set_currency_labels(['total'], 'USD');
        frm.set_currency_labels(['rate', 'amount'], 'USD', 'content');
    },

    refresh: function(frm) {
        // TODO
        frm.dashboard.set_headline('Mensaje humano del estado del paquete?');
    }

});

frappe.ui.form.on('Parcel Content', {
    // Children Doctype of Parcel

    content_remove(frm) {
        calculate_parcel_total(frm);
    },

    rate(frm, cdt, cdn) {
        calculate_parcel_content_amount_and_parcel_total(frm, cdt, cdn);
    },

    qty(frm, cdt, cdn) {
        calculate_parcel_content_amount_and_parcel_total(frm, cdt, cdn);
    },

});
