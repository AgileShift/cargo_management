frappe.ui.form.on('Shipment Receipt', {

    onload: function (frm) {
	    frm.set_query('parcel', 'shipment_receipt_lines', () => {
            return {
                'filters': [
                    ['Parcel', 'status', 'not in', ['Available to Pickup', 'Finished']]
                ]
            };
        });
    },

    shipment: function (frm) {
        frm.clear_table('shipment_receipt_lines');

        // TODO: frappe.show_progress()
        frappe.model.with_doc('Shipment', frm.doc.shipment)
            .then(shipment => shipment.shipment_lines.map(sl => sl.warehouse_receipt)) // Return WRs in Shipment
            .then(warehouse_receipts => { // Read all WR names
                return Promise.all( // Return all promises when completed
                    warehouse_receipts.map(wr => { // Iter all over the WR names
                        frm.add_child('shipment_receipt_warehouse_lines', {'warehouse_receipt': wr}); // TODO: Finish
                        return frappe.model.with_doc('Warehouse Receipt', wr) // Get individual WR Doc
                            .then(wr => wr.warehouse_receipt_lines.map(wrl => wrl.parcel)); // Return parcels names in WR
                    })
                ).then(promises => [].concat.apply([], promises)); // Return all the promises into 1 array
            })
            .then(parcels => { // Read all parcels names
                frappe.show_alert('Adding Parcels.');

                return Promise.all( // Return all promises when completed.
                    parcels.map(parcel_name => { // Iter all over the parcels names
                        return frappe.model.with_doc('Parcel', parcel_name); // Return individual Parcel Doc
                    })
                ).then(promises => promises.sort((a, b) => (a.customer > b.customer) ? 1 : ((b.customer > a.customer) ? -1 : 0)));
            })
            .then(parcels => {
                frappe.show_alert('Parcels added.');

                parcels.forEach(parcel => {
                    let parcel_content = parcel.content.map(c => {
                        return `Descripcion: ${c.description}\nMonto: $${c.amount}`;
                    });

                    frm.add_child('shipment_receipt_lines', { // Add the parcel to the child table
                        'parcel': parcel.name,
                        'customer_name': parcel.customer_name,
                        'carrier_weight': parcel.carrier_est_weight,
                        'content': parcel_content.join('\n\n'),
                    });
                });

                frm.refresh_field('shipment_receipt_warehouse_lines'); // Refresh the child table.
                frm.refresh_field('shipment_receipt_lines'); // Refresh the child table.
        });
    }
});
