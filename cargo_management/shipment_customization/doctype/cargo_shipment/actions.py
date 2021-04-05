import frappe
from frappe import _


@frappe.whitelist()
def mark_cargo_shipment_in_transit(source_name: str):
    doc = frappe.get_doc('Cargo Shipment', source_name)

    doctypes_to_update = {
        # 'Cargo Shipment': {
        #     'new_status': 'In Transit',
        #     'child_doc_lines': doc.get('cargo_shipment_lines'),
        # },
        'Warehouse Receipt': {
            'new_status': 'In Transit',
            'doc_names': doc.get('cargo_shipment_lines'),
            'updated': 0
        },
        'Package': {
            'new_status': 'In Transit',
            'doc_names': doc.get('cargo_shipment_lines'),  # TODO: Gather this data!!
            'updated': 0,
        }
    }

    total_packages = updated_packages = 0  # For Count purposes

    for cs_line in cargo_shipment.cargo_shipment_lines:
        warehouse_receipt = frappe.get_doc('Warehouse Receipt', cs_line.warehouse_receipt)

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

    frappe.msgprint(msg=[
        '{} Warehouse Receipt in transit.'.format(len(cargo_shipment.cargo_shipment_lines)),
        '{} of {} Packages in transit.'.format(updated_packages, total_packages)
    ], title=_('Success'), as_list=True)
#43