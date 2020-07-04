function calculate_parcel_total_amount(frm) {
    // Calculate the total_amount field on Parcel Doctype
    let total_amount = 0;

    $.each(frm.doc.content, function (i, d) {
        total_amount += d.quantity * d.unit_price;
    });

    frm.set_value('total_amount', total_amount);
}

frappe.ui.form.on('Parcel', {

    setup: function (frm) {

        // This allow us to send non-obtrusive messages from the backend: FIXME: is another way? Refactor.
        // https://frappeframework.com/docs/user/en/api/dialog#frappeshow_alert its not available for Python API.
        frappe.realtime.on('display_alert', function (msg) {
            frappe.show_alert({message: msg, indicator: 'yellow'}, 5);
        });

        frappe.realtime.on('new_carrier_data', () => {
            frm.reload_doc(); // On new data. reload form data from db!
        })

    },

});


frappe.ui.form.on('Parcel Content', {
    // Children Doctype of Parcel

    'content_remove': function (frm) {
        calculate_parcel_total_amount(frm);
    },

    'unit_price': function (frm) {
        calculate_parcel_total_amount(frm);
    },

    'quantity': function (frm) {
        calculate_parcel_total_amount(frm);
    },

});
