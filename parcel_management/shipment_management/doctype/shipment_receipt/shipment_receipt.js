frappe.ui.form.on('Shipment Receipt', {

    shipment: function (frm) {
        let warehouse_receipts = [];
        let parcels = []

        frm.clear_table('shipment_receipt_lines');

        // frappe.show_progress()

        frappe.model.with_doc('Shipment', frm.doc.shipment, () => {
            $.each(frappe.model.get_doc('Shipment', frm.doc.shipment).shipment_lines, (i, sl) => {
                warehouse_receipts.push(sl.warehouse_receipt);  // Getting all warehouse Receipts in Shipment
            });
        }).then(() => {
            $.each(warehouse_receipts, (i, wr) => {
                frappe.model.with_doc('Warehouse Receipt', wr, () => {
                    $.each(frappe.model.get_doc('Warehouse Receipt', wr).warehouse_receipt_lines, (i, wrl) => {
                        parcels.push(wrl.parcel);
                    });
                }).then(() => {
                    $.each(parcels, (i, parcel) => {
                        let cd = frm.add_child('shipment_receipt_lines');
                        frappe.get_doc('Parcel')
                        frappe.model.set_value(cd.doctype, cd.name, 'parcel', parcel);
                    });

                    //61290980628043021406

                    frm.refresh_field('shipment_receipt_lines');
                    frm.refresh();
                });
            });
        }).finally(() => {
            console.log(warehouse_receipts);
            console.log(parcels);
        });
    }

});
