import frappe


@frappe.whitelist(allow_guest=False)
def mark_shipment_in_transit(source_name: str):
    """ Used as Action button in Doctype: Change status of the parcels and the warehouses receipts of the shipment. """
    shipment = frappe.get_doc('Shipment', source_name)

    total_parcels = updated_parcels = 0  # For Count purposes

    # Core: Silence Notifications and emails!
    frappe.flags.mute_emails = frappe.flags.in_import = shipment.mute_emails

    for shipment_line in shipment.shipment_lines:
        warehouse_receipt = frappe.get_doc('Warehouse Receipt', shipment_line.warehouse_receipt)

        for wr_line in warehouse_receipt.warehouse_receipt_lines:
            parcel = frappe.get_doc('Parcel', wr_line.parcel)  # Getting Parcel Doctype
            total_parcels += 1

            if parcel.change_status('In Transit'):  # If Status can be changed. To prevent unnecessary updates
                updated_parcels += 1
                parcel.flags.ignore_validate = True  # Set flag ON because Doc will be saved from bulk edit. No validations.
                parcel.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

        # TODO: Maybe make a safe def to prevent unnecessary saves
        warehouse_receipt.status = 'In Transit'
        warehouse_receipt.flags.ignore_validate = True
        warehouse_receipt.save(ignore_permissions=True)

    # TODO: Maybe make a safe def to prevent unnecessary saves
    shipment.status = 'In Transit'
    shipment.flags.ignore_validate = True
    shipment.save(ignore_permissions=True)

    frappe.flags.mute_emails, frappe.flags.in_import = False, False

    frappe.msgprint(msg=[
        '{0} Warehouse Receipt in transit.'.format(len(shipment.shipment_lines)),
        '{0} Parcels changed to in transit of {1}.'.format(updated_parcels, total_parcels)
    ], title='Success')  # FIXME: as_list=True in next updates for production

"""
Shipment
Pasa de in transit, a in customs
Cuanto esta in customs, aparece un boton para crear la hoja de recepcion!

Se crea la hoja de recepcion, que contiene el shipment, los warehouses y los parcels.
Cuando se crea la hoja, todos lo anterior para In Sorting

Cuando se valida la hoja:
EL Shipment y el Warehouse se cierra.

Deespues que la hoja esta validad, aparece un boton de crear facturas
Cuando se crean las facturas, el parcel cambia a Available for Pikcup y se le hace el Link

Cuando Una sales Invoice es Pagada el parcel cambia a Finished.
"""

""" 
Parcels missing on the shipment receipt
Will be changed to: On Hold
"""