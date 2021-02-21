from collections import defaultdict

import frappe


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
                'Descripcion: ', pc.description,
                '\nMonto: $', FORMAT(pc.amount, 2),
                '\nCodigo: ', IFNULL(pc.item_code, '')
                SEPARATOR '\n\n'
            ) AS content
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


# TODO: Crear facturas - Cada Invoice Item: debe de tener package
@frappe.whitelist()
def make_sales_invoice(cargo_shipment_receipt_lines):
    """ Create a sales invoice for each customer with items as packages. From Cargo Shipment Receipt """
    cargo_shipment_receipt_lines = frappe.parse_json(cargo_shipment_receipt_lines)

    # Sorting all the customers data in a single dict
    customers_to_invoice = defaultdict(list)
    for item in cargo_shipment_receipt_lines:
        customer = item.pop('customer')
        customers_to_invoice[customer].append(item)

    # Creating a Sales Invoice for each customer
    for customer in customers_to_invoice:
        sales_invoice = frappe.new_doc('Sales Invoice')
        sales_invoice.customer = customer
        # sales_invoice.company = 'QuickBox Nicaragua'  # TODO
        # sales_invoice.currency = 'USD'   # TODO

        # Iterate over customer items to invoice
        for item in customers_to_invoice[customer]:
            sales_invoice.append('items', {
                'item_code': item.get('item_code'),
                'package': item.get('package'),
                # TODO: Working
                'qty': item.get('gross_weight', 1),
                'rate': item.get('import_price', 1)
            })

        return sales_invoice

        sales_invoice.set_missing_values()
        sales_invoice.save()

        return sales_invoice

    return customers_to_invoice
