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


@frappe.whitelist()
def make_sales_invoice():
    """ Create sales invoice for each customer and packages in the cargo shipment receipt. """
    pass
