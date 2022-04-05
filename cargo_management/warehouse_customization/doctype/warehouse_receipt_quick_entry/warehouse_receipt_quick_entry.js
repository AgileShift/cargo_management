frappe.ui.form.on('Warehouse Receipt Quick Entry', {

    setup(frm) {
        // New Fields
        frm.transportation = frappe.ui.form.make_control({
            parent: frm.fields_dict.transportation_html.$wrapper.addClass('text-center'),
            df: {
                label: __('Transportation'),
                fieldname: 'transportation',
                fieldtype: 'MultiCheck',
                options: [
                    {label: __('SEA'), value: 'Sea'},
                    {label: __('AIR'), value: 'Air'}
                ],
                columns: 2
            }
        });
        frm.size_table = frappe.ui.form.make_control({
            parent: frm.fields_dict.size_table_html.$wrapper,
            df: {
                fieldname: 'sizes_table',
                fieldtype: 'Table',
                fields: [
                    {
                        label: __('Type'),
                        fieldtype: 'Select',
                        fieldname: 'type',
                        in_list_view: true,
                        options: ['Box', 'Envelope', 'Pallet', 'Mail']
                    }
                ].concat(
                    ['Weight (lb)', 'Length (cm)', 'Width (cm)', 'Height (cm)'].map((df) => ({
                        label: __(df),
                        fieldtype: 'Float',
                        fieldname: df.split(' ')[0].toLowerCase(),
                        in_list_view: true,
                        precision: 2
                    }))
                ),
                in_place_edit: true,
                cannot_add_rows: false,
            },
            render_input: true
        });
    },

    refresh(frm) {
        // Customizations
        frm.disable_save();
        frm.page.set_title('');
        frm.size_table.grid.add_new_row();
        frm.fields_dict.carrier.$wrapper.css('margin-top', "var(--margin-lg)");
        frm.fields_dict.warehouse_description.$input.css('height', 'auto');
        frm.fields_dict.customer_description.$wrapper.find('.control-value').css('font-weight', 'bold');
        frm.fields_dict.notes.$input.css('height', 'auto');

        frm.page.set_primary_action(__('Print'), () => frm.events.print_and_save(frm));
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

    // Custom Save
    print_and_save(frm) {
        // Build data
        frm.doc.transportation = frm.transportation.get_value()[0];
        frm.doc.size_table = frm.size_table.get_value();

        frappe.call({
            method: 'cargo_management.warehouse_customization.doctype.warehouse_receipt_quick_entry.warehouse_receipt_quick_entry.create_warehouse_receipt_line_from_quick_entry',
            freeze: true,
            freeze_message: __('Saving Warehouse Receipt...'),
            args: {quick_entry: frm.doc},
            callback: (r) => { // TODO: Maybe a Switch
                console.log(r.message);
            }
        });
    },

    // Custom Functions if a Tracking Number is Found
    show_alerts(frm) {
        frm.dashboard.clear_headline();

        if (frm.doc.customer_description) {
            frm.layout.show_message('<b>No es necesario abrir el paquete. <br> Cliente Pre-Alerto el contenido.</b>', '');
            frm.layout.message.removeClass().addClass('form-message ' + 'green');  // FIXME: Core overrides color
        }
    },

    set_package: function (frm, coincidence) {
        const doc_name = coincidence.name || coincidence;

        frappe.db.get_doc('Package', doc_name).then(function (doc) {
            frm.doc.tracking_number = doc.name;
            frm.doc.customer = doc.customer;
            frm.doc.customer_name = doc.customer_name;
            frm.doc.shipper = doc.shipper;

            //frm.transportation.select_options(doc.transportation);
            $(frm.transportation.$wrapper.find(`:checkbox[data-unit="${doc.transportation}"]`)[0]).trigger('click');

            frm.doc.carrier = doc.carrier;

            frm.doc.customer_description = (doc.content.length > 0) ? doc.content.map(c => 'Item: ' + c.description + '\nCantidad: ' + c.qty).join("\n\n") : null;

            frm.refresh_fields();
            frm.events.show_alerts(frm);
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
    }
});
