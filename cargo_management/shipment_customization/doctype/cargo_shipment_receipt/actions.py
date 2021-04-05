from collections import defaultdict

import frappe
from cargo_management.package_management.doctype.package.utils import get_field_list_from_child_table, change_status


@frappe.whitelist()
def update_status(source_doc_name: str, new_status: str):
    doc = frappe.get_doc('Cargo Shipment Receipt', source_doc_name)  # Getting the Cargo Shipment Receipt Doc.

    # We Mark the actual child tables added to the parent, because we can dynamically add
    change_status(docs_to_update={
        'Cargo Shipment Receipt': {
            'doc_names': [doc.name]
        },
        'Cargo Shipment': {
            'doc_names': [doc.cargo_shipment]
        },
        'Warehouse Receipt': {
            'doc_names': get_field_list_from_child_table(doc.cargo_shipment_receipt_warehouse_lines, 'warehouse_receipt')
        },
        'Package': {
            'doc_names': get_field_list_from_child_table(doc.cargo_shipment_receipt_lines, 'package')
        }
    }, new_status=new_status, msg_title='Marked as Sorting', mute_emails=doc.mute_emails)


@frappe.whitelist()
@frappe.read_only()
def get_packages_and_wr_in_cargo_shipment(cargo_shipment: str):
    """ Get all packages and warehouse receipts connected to a cargo shipment. """

    # Getting all warehouse receipt in a cargo shipment
    wrs = [cs_line.warehouse_receipt for cs_line in
           frappe.get_all('Cargo Shipment Line', fields='warehouse_receipt', filters={'parent': cargo_shipment}, order_by='idx')]

    packages = frappe.db.sql(query="""
        SELECT
            p.name, p.customer_name, p.customer, p.carrier_est_weight,
            GROUP_CONCAT(DISTINCT
                pc.description,
                '\nMonto: $', FORMAT(pc.amount, 2),
                '\nCodigo: ', IFNULL(pc.item_code, '')
                SEPARATOR '\n\n'  # TODO: Add total details from package
            ) AS content,
            p.total
        FROM tabPackage p
            LEFT JOIN `tabPackage Content` pc ON pc.parent = p.name
            INNER JOIN `tabWarehouse Receipt Line` wrl ON wrl.package = p.name
        WHERE wrl.parent IN %(warehouse_receipts)s
        GROUP BY p.name
        ORDER BY p.customer_name
    """, values={
        'warehouse_receipts': wrs
    }, as_dict=True)

    return {
        'packages': packages,
        'warehouse_receipts': wrs,
    }


@frappe.whitelist()
def make_sales_invoice(doc):
    # TODO: Crear facturas - Cada Invoice Item: debe de tener package
    # TODO: Que se guarde el invoice en cada uno, para que no se repita la creacion de cada factura, en cada intento
    # TODO: Set customer if not set!.

    """ Create a sales invoice for each customer with items as packages. From Cargo Shipment Receipt """
    doc = frappe.parse_json(doc)
    cargo_shipment_receipt = frappe.get_doc('Cargo Shipment Receipt', doc.get('name'))

    # Sorting all the customers data in a single dict
    customers_to_invoice = defaultdict(list)
    for item in cargo_shipment_receipt.cargo_shipment_receipt_lines:
        if not item.customer:
            frappe.throw('Agregar cliente a fila: {}, Paquete: {}'.format(item.get('idx'), item.get('package')))

        customers_to_invoice[item.customer].append(item)

    # Creating a Sales Invoice for each customer
    # TODO: Validate fields and throw before start to create sales order!
    for customer in customers_to_invoice:
        sales_invoice = frappe.new_doc('Sales Invoice')
        sales_invoice.customer = customer  # Company and Currency are automatically set

        # Iterate over customer items to invoice
        csrl_invoiced_items = []
        for item in customers_to_invoice[customer]:
            item_data = {  # Always pass this data
                'item_code': item.item_code,
                'package': item.package,
                'qty': item.billable_qty_or_weight,
                'total_weight': item.gross_weight,  # TODO: weight_per_unit
                'description': item.content
            }

            if item.item_price > 0.00:
                item_data.update({'price_list_rate': item.item_price})

            sales_invoice.append('items', item_data)  # Add each items
            csrl_invoiced_items.append(item.name)

        sales_invoice.set_missing_values()
        sales_invoice.save(ignore_permissions=True)  # Saving a invoice as draft

        for item in csrl_invoiced_items:
            frappe.db.set_value('Cargo Shipment Receipt Line', item, 'sales_invoice', sales_invoice.name, update_modified=False)

    cargo_shipment_receipt.notify_update()
    cargo_shipment_receipt.save(ignore_permissions=True)  # Send update notify

    return customers_to_invoice  # TODO: Return the new sales invoice and update the cargo shipment table!!!.
