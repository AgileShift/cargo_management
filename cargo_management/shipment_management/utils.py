import frappe


@frappe.whitelist(methods='GET')
def get_packages_and_wr_in_cargo_shipment(cargo_shipment: str):
    """ Get all packages and warehouse receipts connected to a cargo shipment. """

    # TODO: Delete: wrs and warehouse_receipts in sql
    wrs = frappe.get_all('Cargo Shipment Line', fields='warehouse_receipt', filters={'parent': cargo_shipment}, order_by='idx', pluck='warehouse_receipt')

    # TODO: WORKING: OPTIMIZE FULL
    packages = frappe.db.sql("""
        SELECT
            p.name, p.customer, p.customer_name, p.carrier_est_weight, p.total,
            GROUP_CONCAT(DISTINCT
                pc.description,
                '\nMonto: $', FORMAT(pc.amount, 2),
                '\nCodigo: ', IFNULL(pc.item_code, ''),
                '\nTarifa: ', FORMAT(pc.import_rate, 2),
                '\nNotas: ', IFNULL(p.notes, '')
                SEPARATOR '\n\n'
            ) AS customer_description#,
            # wrl.wr_reference, wrl.description as warehouse_description
        FROM tabPackage p
            LEFT JOIN `tabPackage Content` pc ON pc.parent = p.name
            INNER JOIN `tabCargo Shipment Line` csl ON csl.package = p.name
        WHERE csl.parent = %(cargo_shipment)s
        GROUP BY p.name
        ORDER BY p.customer_name
    """, {
        'cargo_shipment': cargo_shipment
    }, as_dict=True)

    return {
        'packages': packages
    }
