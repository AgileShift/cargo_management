frappe.ui.form.on('Cargo Packing List', {
	refresh: function(frm) {
	    frm.page.add_action_icon('printer', () => {
            frm.print_doc();
			// frm.trigger('cargo_shipment');
	    }, '', __('Print'));
	},

	cargo_shipment: function (frm) {
		if (!frm.doc.cargo_shipment) {
            return;
        }

		frm.clear_table('content');

		frappe.call({
			method: 'cargo_management.shipment_customization.utils.get_packages_and_wr_in_cargo_shipment',
            args: {cargo_shipment: frm.doc.cargo_shipment},
            freeze: true,
            freeze_message: __('Adding Packages...'),
		}).then(r => {

			r.message.packages.forEach(package_doc => {
                frm.add_child('content', {
					'wr_reference': package_doc.wr_reference,
                    'package': package_doc.name,
                    'consignee': package_doc.customer_name,
                    'customer_description': package_doc.customer_description,
					'warehouse_description': package_doc.warehouse_description,
					'total': package_doc.total
                });
            });

			frm.refresh_field('content');
		});
	}

});
