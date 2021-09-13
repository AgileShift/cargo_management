import frappe


@frappe.whitelist(methods='GET')
def get_packages_and_wr_in_cargo_shipment(cargo_shipment: str):
    """ Get all packages and warehouse receipts connected to a cargo shipment. """

    wrs = frappe.get_all('Cargo Shipment Line', fields='warehouse_receipt', filters={'parent': cargo_shipment}, order_by='idx', pluck='warehouse_receipt')

    # TODO: WORKING
    packages = frappe.db.sql("""
        SELECT
            p.name, p.customer, p.customer_name, p.carrier_est_weight, p.total,
            GROUP_CONCAT(DISTINCT
                pc.description,
                '\nMonto: $', FORMAT(pc.amount, 2),
                '\nCodigo: ', IFNULL(pc.item_code, '')
                SEPARATOR '\n\n'  # TODO: Add total details from package
            ) AS customer_description,
            wrl.wr_reference, wrl.description as warehouse_description
        FROM tabPackage p
            LEFT JOIN `tabPackage Content` pc ON pc.parent = p.name
            INNER JOIN `tabWarehouse Receipt Line` wrl ON wrl.package = p.name
        WHERE wrl.parent IN %(warehouse_receipts)s
        GROUP BY p.name
        ORDER BY p.customer_name
    """, {
        'warehouse_receipts': wrs
    }, as_dict=True)

    return {
        'packages': packages,
        'warehouse_receipts': wrs,
    }
