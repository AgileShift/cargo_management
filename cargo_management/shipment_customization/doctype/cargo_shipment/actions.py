import frappe
from frappe import _


@frappe.whitelist(allow_guest=False)
def mark_cargo_shipment_in_transit(source_name: str):
    """ Used as Action button in Doctype: Change status of the packages and the warehouses receipts of the cargo shipment """
    cargo_shipment = frappe.get_doc('Cargo Shipment', source_name)

    total_packages = updated_packages = 0  # For Count purposes

    # Core: Silence Notifications and emails!
    frappe.flags.mute_emails = frappe.flags.in_import = cargo_shipment.mute_emails

    for cargo_shipment_line in cargo_shipment.cargo_shipment_lines:
        warehouse_receipt = frappe.get_doc('Warehouse Receipt', cargo_shipment_line.warehouse_receipt)

        for wr_line in warehouse_receipt.warehouse_receipt_lines:
            package = frappe.get_doc('Package', wr_line.package)  # Getting Package Doctype
            total_packages += 1

            if package.change_status('In Transit'):  # If Status can be changed. To prevent unnecessary updates
                updated_packages += 1
                package.flags.ignore_validate = True  # Set flag ON because Doc will be saved from bulk edit. No validations.
                package.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

        # TODO: Maybe make a safe def to prevent unnecessary saves. Like change_status?
        warehouse_receipt.status = 'In Transit'
        warehouse_receipt.flags.ignore_validate = True
        warehouse_receipt.save(ignore_permissions=True)

    # TODO: Maybe make a safe def to prevent unnecessary saves
    cargo_shipment.status = 'In Transit'
    cargo_shipment.flags.ignore_validate = True
    cargo_shipment.save(ignore_permissions=True)

    frappe.flags.mute_emails, frappe.flags.in_import = False, False

    frappe.msgprint(msg=[
        '{0} Warehouse Receipt in transit.'.format(len(cargo_shipment.shipment_lines)),
        '{0} Packages changed to in transit of {1}.'.format(updated_packages, total_packages)
    ], title=_('Success'), as_list=True)
