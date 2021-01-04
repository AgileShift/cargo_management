frappe.ui.form.on('Cargo Shipment Receipt', {

    setup: function (frm) {
        // TODO: this must be running from core frappe code. Some glitch make us hardcoded the realtime handler here.
        frappe.realtime.on('doc_update', () => { // See: https://github.com/frappe/frappe/pull/11137
            frm.reload_doc(); // Reload form UI data from db.
        });
    },

    onload: function (frm) {
	    frm.set_query('package', 'cargo_shipment_receipt_lines', () => {
            return {
                filters: {
                    status: ['not in', ['Available to Pickup', 'Finished']]
                }
            };
        });
    },

    cargo_shipment: function (frm) {
        frm.clear_table('cargo_shipment_receipt_lines');

        // TODO: frappe.show_progress()
        frappe.model.with_doc('Cargo Shipment', frm.doc.cargo_shipment)
            .then(shipment => shipment.cargo_shipment_lines.map(sl => sl.warehouse_receipt)) // Return WRs in Shipment
            .then(warehouse_receipts => { // Read all WR names
                return Promise.all( // Return all promises when completed
                    warehouse_receipts.map(wr => { // Iter all over the WR names
                        // frm.add_child('shipment_receipt_warehouse_lines', {'warehouse_receipt': wr}); // TODO: Finish
                        return frappe.model.with_doc('Warehouse Receipt', wr) // Get individual WR Doc
                            .then(wr => wr.warehouse_receipt_lines.map(wrl => wrl.package)); // Return packages names in WR
                    })
                ).then(promises => [].concat.apply([], promises)); // Return all the promises into 1 array
            })
            .then(packages => { // Read all packages names
                frappe.show_alert('Adding Packages.');
                return Promise.all( // Return all promises when completed.
                    packages.map(package_name => { // Iter all over the packages names
                        return frappe.model.with_doc('Package', package_name); // Return individual Package Doc
                    })
                ).then(promises => promises.sort((a, b) => (a.customer > b.customer) ? 1 : ((b.customer > a.customer) ? -1 : 0)));
            })
            .then(packages => {
                frappe.show_alert('Packages added.');

                packages.forEach(package_doc => {
                    let package_content = package_doc.content.map(c => {
                        return `Descripcion: ${c.description}\nMonto: $${c.amount}`;
                    });

                    frm.add_child('cargo_shipment_receipt_lines', { // Add the package to the child table
                        'package': package_doc.name,
                        'customer_name': package_doc.customer_name,
                        'carrier_weight': package_doc.carrier_est_weight,
                        'content': package_content.join('\n\n'),
                    });
                });

                frm.refresh_field('cargo_shipment_receipt_warehouse_lines'); // Refresh the child table.
                frm.refresh_field('cargo_shipment_receipt_lines'); // Refresh the child table.
        });
    }
});
