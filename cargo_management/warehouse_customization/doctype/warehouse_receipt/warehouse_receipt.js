frappe.ui.form.on('Warehouse Receipt', {

    transportation_multi_check: function (frm) {
        frm.transportation = frappe.ui.form.make_control({
            parent: frm.fields_dict.transportation_multicheck_html.$wrapper.addClass('text-center'),
            df: {
                label: __('Transportation Method'),
                fieldtype: 'MultiCheckUnique',
                reqd: true,
                columns: 2,
                options: [{label: __('SEA'), value: 'Sea'}, {label: __('AIR'), value: 'Air'}],
                on_change: (selected) => frm.doc.transportation = selected
            }
        });
    },

    setup: function (frm) {
        $('.layout-side-section').hide(); // Little Trick to work better

        if (frm.is_new())
            frm.events.transportation_multi_check(frm);
    },

    onload_post_render: function (frm) {
        if (frm.is_new())
            frm.grids[0].grid.add_new_row();

        frm.events.print_iframe(frm); // todo delete
    },

    before_save: function (frm) {
        frm.print_label = frm.is_new(); // If new true else undefined
    },

    after_save: function (frm) {
        if (!frm.print_label) {
            return;
        }

        //http://localhost:8000/printview?doctype=Warehouse%20Receipt&name=ae547156cc&trigger_print=1&format=Standard&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=en-US

        window.open(
            frappe.urllib.get_full_url(
                'printview?doctype=Warehouse%20Receipt&name=' + frm.doc.name +
                '&trigger_print=1&format=Warehouse%20Receipt%20Labels&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=es'
            ) // Emulating print.js inside frappe/printing/page/print/print.js
        );
    },

    print_iframe: function (frm) {
        // Improve Print Format
        // No more JSBarcode or better to embeed?
        // After save call in frame!
        // New doc after print
        // https://stackoverflow.com/questions/2578052/printing-contents-of-another-page
        // https://discuss.erpnext.com/t/how-to-generate-barcodes-in-erpnext-using-jsbarcode-library/45573/3
        /*
            5. Mejoras solicitadas por Joshua
              Para crear el warehouse - para imprimir
              para imprimir el warehouse en fisico: cuando hace una entrega
              que le abra a nueva pantalla
         */
        frm.$wrapper.append(
            "<iframe name='print_frame' src='http://localhost:8000/printview?doctype=Warehouse%20Receipt&name=WR-14569&format=Warehouse%20Receipt%20Labels&no_letterhead=1'></iframe>"
        );
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
            callback: (r) => { // TODO: Maybe a Switch
                if (r.message.coincidences) {
                    frm.events.show_selector_dialog(frm, r.message);
                } else if (r.message.coincidence) {
                    frappe.show_alert('Paquete Pre-Alertado.');
                    frm.events.set_package(frm, r.message.coincidence);
                } else {
                    frappe.show_alert('Paquete sin Pre-Alerta.');
                }
            }
        });
    },

    // Custom Functions
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
            no_cancel_flag: true,  // Cannot cancel with keyboard
            size: 'extra-large',
            fields: [{fieldtype: 'HTML', fieldname: 'table_html'}]
        });

        selector_dialog.fields_dict.table_html.$wrapper
            .html(frappe.render_template('package_selector', {
                search_term: opts.search_term,
                coincidences: opts.coincidences
            }))
            .find('a').on('click', e => {
                e.preventDefault();
                selector_dialog.hide();
                frm.events.set_package(frm, $(e.target).attr('data-value'));
            });

        selector_dialog.show();
    },

    set_package: function (frm, coincidence) {
        const doc_name = coincidence.name || coincidence;

        frappe.db.get_doc('Package', doc_name).then(doc => {
            frm.doc.tracking_number = doc.name;
            frm.doc.carrier = doc.carrier;

            frm.transportation.$checkbox_area.find(`:checkbox[data-unit="${doc.transportation}"]`).trigger('click'); // This Trigger on_change

            // FIXME: Join this fields?
            frm.doc.shipper = doc.shipper;
            frm.doc.consignee = doc.customer_name;

            frm.doc.customer_description = (doc.content.length > 0) ? doc.content.map(c => 'Item: ' + c.description + '\nCantidad: ' + c.qty).join("\n\n") : null;

            frm.refresh_fields();
            frm.events.show_alerts(frm); // FIXME: Work on this
        });
    },

    show_alerts(frm) {
        // TODO: Make this come from API?
        frm.dashboard.clear_headline();

        if (frm.doc.customer_description) {
            frm.layout.show_message('<b>No es necesario abrir el paquete. <br> Cliente Pre-Alerto el contenido.</b>', '');
            frm.layout.message.removeClass().addClass('form-message ' + 'green');  // FIXME: Core overrides color
        }
    },
});

frappe.ui.form.on('Warehouse Receipt Line', {});

// https://stackoverflow.com/a/1977126/3172310 -> When a Button is in a Table
//$(document).on('keydown', "input[data-fieldname='tracking_number'], input[data-fieldname='weight'], " +
//    "input[data-fieldname='length'], input[data-fieldname='width'], input[data-fieldname='height']", (event) => {
//    if (event.key === 'Enter') {  // Enter key is sent if field is set from barcode scanner.
//        event.preventDefault(); // We prevent the button 'Attach Image' opens a pop-up.
//    }
//});