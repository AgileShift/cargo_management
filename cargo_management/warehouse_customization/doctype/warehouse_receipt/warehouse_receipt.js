frappe.ui.form.on('Warehouse Receipt', {

    ask_transportation_type: function (frm) {
        const transport_dialog = new frappe.ui.Dialog({
            title: __('Select Transportation Type'),
            fields: [
                {
                    fieldname: 'sea_transport', fieldtype: 'Check', label: __('Sea Transport'),
                    change: () => cur_dialog.fields_dict.air_transport.input.checked = !cur_dialog.get_value('sea_transport')
                }, {fieldtype: 'Column Break'}, {
                    fieldname: 'air_transport', fieldtype: 'Check', label: __('Air Transport'),
                    onchange: () => cur_dialog.fields_dict.sea_transport.input.checked = !cur_dialog.get_value('air_transport')
                }
            ],
            no_cancel_flag: true,  // Cannot cancel with keyboard
            static: true,          // Cannot cancel touching outside pop-up
            primary_action_label: __('Select'),
            primary_action: (response) => {
                const transport_type = response.sea_transport ? 'Sea' : response.air_transport ? 'Air' : false;
                if (!transport_type) {
                    frappe.throw({message: 'Seleccione un tipo de transporte.', alert: true});
                }
                transport_dialog.hide();
                frm.set_value('transportation_type', transport_type);  // Trigger the event that opens first row
            }
        });
        transport_dialog.show();
    },

    setup: function () {
        $('.layout-side-section').hide(); // Little Trick to work better

        // https://stackoverflow.com/a/1977126/3172310
        $(document).on('keydown', "input[data-fieldname='tracking_number'], input[data-fieldname='weight'], " +
            "input[data-fieldname='length'], input[data-fieldname='width'], input[data-fieldname='height']", (event) => {
            if (event.key === 'Enter') {  // Enter key is sent if field is set from barcode scanner.
                event.preventDefault(); // We prevent the button 'Attach Image' opens a pop-up.
            }
        });
    },

    onload: function (frm) {
        // if (frm.is_new()) frm.events.ask_transportation_type(frm);
    },

    before_save: function (frm) {
        // Calculate fields from child so can be saved from client-side
        frm.set_value('warehouse_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'warehouse_est_weight'));
        frm.set_value('carrier_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'carrier_est_weight'));

        frm.print_label = frm.is_new(); // If new true else undefined.
    },

    after_save: function (frm) {
        if (!frm.print_label) return;

        window.open(
            frappe.urllib.get_full_url(
                'printview?doctype=Warehouse%20Receipt&name=' + frm.doc.name +
                '&trigger_print=1&format=Warehouse%20Receipt%20Labels&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=es'
            ) // Emulating print.js inside frappe/printing/page/print/print.js
        );
    },

    transportation_type: function (frm) {
        frm.fields_dict.warehouse_receipt_lines.grid.grid_rows[0].show_form();  // frm.grids[0].grid.grid_rows[0].show_form();
    },
});

//95

// Child Table
frappe.ui.form.on('Warehouse Receipt Line', {

    package: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];

// 9400108205498583611457
// 92748902712008583188149716
// 92612902712008583186800743
// 4203316692612927005455000268974896

        frappe.db.get_list('Package',{
            filters: {
                name: ["like", "%" + row.package + "%"]
            }
        }).then(docs => {
            if (docs) {
                frappe.msgprint('Hay varios opciones' + docs)
            }
            return;
            row.transportation_type = doc.transportation_type;
            row.customer = doc.customer;
            row.customer_name = doc.customer_name;
            row.carrier = doc.carrier;
            row.customer_description = doc.content.map(c => 'Item: ' + c.description + '\nCantidad: ' + c.qty).join("\n\n");
            row.carrier_real_delivery = doc.carrier_real_delivery;
            row.carrier_est_weight = doc.carrier_est_weight;

            frm.refresh_field('warehouse_receipt_lines');
        });
    },

    warehouse_est_weight: function (frm) {
        // TODO: Work this?
        frm.set_value('warehouse_est_gross_weight', frm.get_sum('warehouse_receipt_lines', 'warehouse_est_weight'));
    }
});

//106  123456789

// TODO: Work This out: onload()
// frm.set_query('package', 'warehouse_receipt_lines', () => {
//     return {
//         filters: {
//             status: ['not in', ['Awaiting Departure', 'In Transit', 'In Customs', 'Sorting', 'Available to Pickup', 'Finished']]
//         }
//     };
// });
