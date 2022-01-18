frappe.ui.form.on('Warehouse Receipt', {

    setup: function () {
        $('.layout-side-section').hide(); // Little Trick to work better

        // https://stackoverflow.com/a/1977126/3172310
        $(document).on('keydown', "input[data-fieldname='tracking_number'], input[data-fieldname='weight'], " +
            "input[data-fieldname='length'], input[data-fieldname='width'], input[data-fieldname='height']", (event) => {
                if (event.key === 'Enter') {  // Enter key is sent if field is set from barcode scanner.
                    event.preventDefault(); // We prevent the button 'Attach Image' opens a pop-up.
                }
            });
    },

    onload: function (frm) {
        // TODO: Work This out
	    // frm.set_query('package', 'warehouse_receipt_lines', () => {
        //     return {
        //         filters: {
        //             status: ['not in', ['Awaiting Departure', 'In Transit', 'In Customs', 'Sorting', 'Available to Pickup', 'Finished']]
        //         }
        //     };
        // });
    },

    refresh: function (frm) {
        // TODO: Add intro message when the warehouse is on cargo_shipment!
        // TODO: Add Progress: dashboard.add_progress or frappe.chart of type: percentage

        if (frm.is_new()) {
            return;
        }

        // TODO: Work on this: will be used now?
        if (frm.doc.status === 'Awaiting Departure') {}
    },

    before_save: function (frm) {
        // Calculate fields from child so can be saved from client-side
        frm.set_value('warehouse_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'warehouse_est_weight'));
        frm.set_value('carrier_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'carrier_est_weight'));

        frm.print_label = frm.is_new(); // If new true else undefined.
    },

    after_save: function (frm) {
        if (!frm.print_label) return;

        window.open(
            frappe.urllib.get_full_url(
                'printview?doctype=Warehouse%20Receipt&name=' + frm.doc.name +
                '&trigger_print=1&format=Warehouse%20Receipt%20Labels&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=es'
            ) // Emulating print.js inside frappe/printing/page/print/print.js
        );
    }
});

// Child Table
frappe.ui.form.on('Warehouse Receipt Line', {
    warehouse_est_weight: function (frm) {
        // TODO: Work this?
        frm.set_value('warehouse_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'warehouse_est_weight'));
    }
});