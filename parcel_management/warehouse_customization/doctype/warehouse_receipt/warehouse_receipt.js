// Copyright (c) 2020, Agile Shift and contributors
// For license information, please see license.txt

frappe.ui.form.on('Warehouse Receipt', {
	onload: function (frm) {

	    // Setting Custom Query
	    frm.set_query('warehouse_receipt_lines', () => {
            return {
                'filters': [
                    ['Parcel', 'status', 'not in', ['Available to Pickup', 'Finished']]
                ]
            };
        });

    }

});
