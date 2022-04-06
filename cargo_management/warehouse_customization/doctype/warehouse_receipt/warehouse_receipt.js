frappe.ui.form.on('Warehouse Receipt', {

    transportation_multi_check: function (frm) {
        frm.transportation_multicheck = frappe.ui.form.make_control({
            parent: frm.fields_dict.transportation_multicheck_html.$wrapper.addClass('text-center'),
            df: {
                label: __('Transportation Method'),
                fieldtype: 'MultiCheck',
                reqd: true,
                columns: 2,
                options: [{label: __('SEA'), value: 'Sea'}, {label: __('AIR'), value: 'Air'}],
                on_change: () => frm.doc.transportation = frm.transportation_multicheck.get_value().at(-1)
            }
        });
        frm.transportation_multicheck.$label.addClass('reqd');
    },

    setup: function (frm) {
        $('.layout-side-section').hide(); // Little Trick to work better

        if (frm.is_new()) {
            frm.events.transportation_multi_check(frm);
        }

        frm.set_df_property('warehouse_receipt_lines', 'reqd', false);
    },

    onload: function (frm) {
        //frm.grids[0].df.in_place_edit = true;
        frm.set_df_property('warehouse_receipt_lines', 'reqd', false);
    },

    refresh: function (frm) {
        if (frm.is_new()) {
            frm.page.set_title('');
        }

        frm.set_df_property('warehouse_receipt_lines', 'reqd', false);



        frm.grids[0].df.reqd = true;

        //frm.grids[0].grid.add_new_row();
        //frm.fields_dict.warehouse_receipt_lines.grid.add_new_row();

        // Customizations
        frm.fields_dict.warehouse_description.$input.css('height', 'auto');
        frm.fields_dict.customer_description.$wrapper.find('.control-value').css('font-weight', 'bold');
        frm.fields_dict.carrier_label_img.$wrapper.css('margin-top', 'var(--margin-xl)')
        frm.fields_dict.notes.$input.css('height', 'auto');
    },

    onload_post_render: function (frm) {
          frm.set_df_property('warehouse_receipt_lines', 'reqd', false);
    },

    before_save: function (frm) {
        // TODO: Recalculate this fields!
        // Calculate fields from child so can be saved from client-side
        frm.set_value('warehouse_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'warehouse_est_weight'));
        frm.set_value('carrier_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'carrier_est_weight'));

        frm.print_label = frm.is_new(); // If new true else undefined.
    },

    after_save: function (frm) {
        // TODO CHECK THIS IS VALID!
        if (!frm.print_label) {
            return;
        }

        window.open(
            frappe.urllib.get_full_url(
                'printview?doctype=Warehouse%20Receipt&name=' + frm.doc.name +
                '&trigger_print=1&format=Warehouse%20Receipt%20Labels&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=es'
            ) // Emulating print.js inside frappe/printing/page/print/print.js
        );
    },

});

// Improve
function set_details(frm, row, coincidence) {
    const doc_name = coincidence.name || coincidence;
    frappe.db.get_doc('Package', doc_name).then(function (doc) {
        row.package = doc.name;
        row.transportation = doc.transportation;
        row.customer = doc.customer;
        row.customer_name = doc.customer_name;
        row.carrier = doc.carrier;
        row.customer_description = doc.content.map(c => 'Item: ' + c.description + '\nCantidad: ' + c.qty).join("\n\n");
        row.carrier_real_delivery = doc.carrier_real_delivery;
        row.carrier_est_weight = doc.carrier_est_weight;

        frm.refresh_fields();
        // frm.refresh_field('warehouse_receipt_lines') // TODO: Change for grid refresh!
    });
}

// Child Table
frappe.ui.form.on('Warehouse Receipt Line', {

    package_selector_dialog: function (frm, packages) {
        const fields = packages.map((package_doc, i) => {
            return {
                fieldname: 'package_option_' + i, fieldtype: 'Check', label: package_doc
            }
        });

        const selector_dialog = new frappe.ui.Dialog({
            title: __('Coincidences found. Please select one.'),
            fields: fields
        })

        selector_dialog.show();
    },

    package: function (frm, cdt, cdn) {
        let row_package = locals[cdt][cdn].package.trim().toUpperCase();  // Sanitize field

        if (!row_package) {
            return;
        }

        frappe.call({
            method: 'cargo_management.warehouse_customization.doctype.warehouse_receipt.actions.find_package_by_tracking_number',
            type: 'GET',
            freeze: true,
            freeze_message: __('Searching Package...'),
            args: {tracking_number: row_package},
            callback: (r) => {

                // https://frappeframework.com/docs/v13/user/en/api/controls & https://frappeframework.com/docs/v13/user/en/api/dialog
                // MultiselectDialog with Package List -> Issue: can select multiple
                // Dialog with a Table Field of Package List -> Issue: can select multiple and needs a select button
                // MultiCheck Field with Package List as Options -> Issue: can select multiple. No extra data for package identification
                // Select Field with Package List as Options -> Issue: Small extra data for package identification, and need a select button or event trigger.
                // LinkSelector with Package List as Options -> Issue: its exactly what we need. But without search and button and configurable extra fields
                if (r.message.coincidences) {
                    return;
                    const selector_dialog = new frappe.ui.Dialog({
                        title: __('Coincidences found for: {0}', [row_package]),
                        static: true,          // Cannot cancel touching outside pop-up
                        size: 'extra-large',
                        fields: [{fieldtype: 'HTML', fieldname: 'table_html',}]
                    });

                    selector_dialog.fields_dict.table_html.$wrapper
                        .html(frappe.render_template('package_selector', {search_term: r.message.search_term, coincidences: r.message.coincidences}))
                        .find('a').on('click', function(e) {
                            e.preventDefault();
                            set_details(frm, locals[cdt][cdn], $(this).attr('data-value'))

                            selector_dialog.hide();
                    });

                    selector_dialog.show();
                } else if (r.message.coincidence) {
                    set_details(frm, locals[cdt][cdn], r.message.coincidence); // FIXME: Fetch row and row_package.
                    frappe.show_alert('Paquete Pre-Alertado');
                } else {
                    frappe.show_alert('Paquete sin Pre-Alerta');
                    frm.refresh_fields(); // This is to recall all evals on depends_on fields. FIXME: Its another way!
                }
            }
        });  //177 -> 156

    },

    warehouse_est_weight: function (frm) {
        // TODO: Work this?
        frm.set_value('warehouse_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'warehouse_est_weight'));
    }
}); // FIXME: 167 . Improve and remove code!

//106 -> 123 -> 196

// Unused Utils

// frm.set_query('package', 'warehouse_receipt_lines', () => {
//     return {
//         filters: {
//             status: ['not in', ['Awaiting Departure', 'In Transit', 'In Customs', 'Sorting', 'Available to Pickup', 'Finished']]
//         }
//     };
// });

//ask_transportation: function (frm) {
//    const transport_dialog = new frappe.ui.Dialog({
//        title: __('Select Transportation Type'),
//        fields: [
//            {
//                fieldname: 'sea_transport', fieldtype: 'Check', label: __('Sea Transport'),
//                change: () => cur_dialog.fields_dict.air_transport.input.checked = !cur_dialog.get_value('sea_transport')
//            }, {fieldtype: 'Column Break'}, {
//                fieldname: 'air_transport', fieldtype: 'Check', label: __('Air Transport'),
//                 onchange: () => cur_dialog.fields_dict.sea_transport.input.checked = !cur_dialog.get_value('air_transport')
//             }
//         ],
//         static: true,          // Cannot cancel touching outside pop-up
//         no_cancel_flag: true,  // Cannot cancel with keyboard
//         primary_action_label: __('Select'),
//         primary_action: (response) => {
//             const transport_type = response.sea_transport ? 'Sea' : response.air_transport ? 'Air' : false;
//             if (!transport_type) {
//                 frappe.throw({message: 'Seleccione un tipo de transporte.', alert: true});
//             }
//             transport_dialog.hide();
//             frm.set_value('transportation', transport_type);  // Trigger the event that opens first row
//         }
//     });
//     transport_dialog.show();
// },

// https://stackoverflow.com/a/1977126/3172310 -> When a Button is in a Table
//$(document).on('keydown', "input[data-fieldname='tracking_number'], input[data-fieldname='weight'], " +
//    "input[data-fieldname='length'], input[data-fieldname='width'], input[data-fieldname='height']", (event) => {
//    if (event.key === 'Enter') {  // Enter key is sent if field is set from barcode scanner.
//        event.preventDefault(); // We prevent the button 'Attach Image' opens a pop-up.
//    }
//});