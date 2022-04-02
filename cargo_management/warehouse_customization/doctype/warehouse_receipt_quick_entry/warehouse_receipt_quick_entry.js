frappe.ui.form.on('Warehouse Receipt Quick Entry', {

    show_alerts(frm) {
        console.log('Show ALerts');
        if (frm.doc.customer_description) {
            frm.set_intro('No es necesario abrir el paquete');
        }
    },

    set_package: function (frm, coincidence) {
        const doc_name = coincidence.name || coincidence;

        // TODO: Improve this?
        frappe.db.get_doc('Package', doc_name).then(function (doc) {
            frm.doc.tracking_number = doc.name;
            //frm.doc.transportation_type = doc.transportation_type;
            frm.doc.customer = doc.customer;
            frm.doc.customer_name = doc.customer_name;
            frm.doc.carrier = doc.carrier;

            if (doc.content.length > 0) { // Has Content
                frm.doc.customer_description = doc.content.map(c => 'Item: ' + c.description + '\nCantidad: ' + c.qty).join("\n\n");
                frm.set_df_property('warehouse_description', 'read_only', true);
            }

            frm.refresh_fields();


        });
    },

    show_selector_dialog: function (frm, opts) {
        // https://frappeframework.com/docs/v13/user/en/api/controls & https://frappeframework.com/docs/v13/user/en/api/dialog
        // MultiselectDialog with Package List -> Issue: can select multiple
        // Dialog with a Table Field of Package List -> Issue: can select multiple and needs a select button
        // MultiCheck Field with Package List as Options -> Issue: can select multiple. No extra data for package identification
        // Select Field with Package List as Options -> Issue: Small extra data for package identification, and need a select button or event trigger.
        // LinkSelector with Package List as Options -> Issue: its exactly what we need. But without search and button and configurable extra fields

        const selector_dialog = new frappe.ui.Dialog({
            title: __('Coincidences found for: {0}', [frm.doc.tracking_number]),
            static: true,          // Cannot cancel touching outside pop-up
            size: 'extra-large',
            fields: [{fieldtype: 'HTML', fieldname: 'table_html'}]
        });

        selector_dialog.fields_dict.table_html.$wrapper
            .html(frappe.render_template('package_selector', {
                search_term: opts.search_term,
                coincidences: opts.coincidences
            }))
            .find('a').on('click', function (e) {
                e.preventDefault();
                selector_dialog.hide();
                frm.events.set_package(frm, $(this).attr('data-value'));
            });

        selector_dialog.show();
    },

    tracking_number: function (frm) {
        frm.doc.tracking_number = frm.doc.tracking_number.trim().toUpperCase();  // Sanitize field

        if (!frm.doc.tracking_number) {
            return;
        }

        frappe.call({
            method: 'cargo_management.warehouse_customization.doctype.warehouse_receipt.actions.find_package_by_tracking_number',
            type: 'GET',
            freeze: true,
            freeze_message: __('Searching Package...'),
            args: {tracking_number: frm.doc.tracking_number},
            callback: (r) => {
                if (r.message.coincidences) {
                    frm.events.show_selector_dialog(frm, r.message);
                } else if (r.message.coincidence) {
                    frappe.show_alert('Paquete Pre-Alertado.');
                    frm.events.set_package(frm, r.message.coincidence);
                } else {
                    frappe.show_alert('Paquete sin Pre-Alerta.');
                    // frm.refresh_fields(); // This is to recall all evals on depends_on fields. FIXME: Its another way!
                }
            }
        });
    }
});
