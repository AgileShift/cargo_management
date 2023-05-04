frappe.ui.form.on('Package Settings', {});

frappe.ui.form.on('Package Carrier', {
    tracking_urls: function (frm, cdt, cdn) {
        let carrier = locals[cdt][cdn];

        // TODO: Validate JSON.parse(tracking_urls) && Validate only for []Arrays not {}Object
        carrier.tracking_urls = carrier.tracking_urls.trim();

        refresh_field('tracking_urls', cdn, 'carriers');
    }
});
