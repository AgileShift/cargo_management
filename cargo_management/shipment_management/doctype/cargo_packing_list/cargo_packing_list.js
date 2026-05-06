frappe.ui.form.on('Cargo Packing List', {
	refresh: function(frm) {
	    frm.page.add_action_icon('printer', () => {
            frm.print_doc();
	    }, '', __('Print'));
	},

	cargo_shipment: function (frm) {
		if (!frm.doc.cargo_shipment) {
            return;
        }

		frm.clear_table('content');

		frappe.call({
			method: 'cargo_management.shipment_management.utils.get_parcels_and_wr_in_cargo_shipment',
			type: 'GET',
            args: {cargo_shipment: frm.doc.cargo_shipment},
            freeze: true,
            freeze_message: __('Adding Parcels...'),
		}).then(r => {
			r.message.parcels.forEach(parcel => {
                frm.add_child('content', {
					'wr_reference': parcel.wr_reference,
                    'package': parcel.name,
                    'consignee': parcel.customer_name,
                    'customer_description': parcel.customer_description,
					'warehouse_description': parcel.warehouse_description,
					'total': parcel.total
                });
            });

			frm.refresh_field('content');
		});
	}

});
