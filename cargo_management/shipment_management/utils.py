import frappe


@frappe.whitelist(methods='GET')
def get_packages_and_wr_in_cargo_shipment(cargo_shipment: str):
    """ Get all packages and warehouse receipts connected to a cargo shipment. """

    # TODO: Delete: wrs and warehouse_receipts in sql
    # wrs = frappe.get_all('Cargo Shipment Line', fields='warehouse_receipt', filters={'parent': cargo_shipment}, order_by='idx', pluck='warehouse_receipt')

    # TODO: WORKING: OPTIMIZE FULL
    packages = frappe.db.sql("""
        SELECT
            p.name, p.customer, p.customer_name, p.carrier_est_weight,
            GROUP_CONCAT(DISTINCT
                pc.description,
                CONCAT('\nVia: ',      IF(p.transportation = 'Air', 'Aereo', 'Maritimo')),

                IF(pc.amount > 0,      CONCAT('\nValor Declarado: $', FORMAT(pc.amount, 2)), ''),
                IF(pc.item_code > '',  CONCAT('\nCodigo: ', pc.item_code), ''),
                IF(pc.import_rate > 0, CONCAT('\nTarifa: $', FORMAT(pc.import_rate, 2)), ''),

                IF(p.name != p.tracking_number, CONCAT('\nNumero de Rastreo: ', p.tracking_number), ''),
                IF(p.consolidated_tracking_numbers > '', CONCAT('\nConsolidados: ', p.consolidated_tracking_numbers), '')

                SEPARATOR '\n\n'
            ) AS customer_description
        FROM tabParcel p
            LEFT JOIN `tabParcel Content` pc ON pc.parent = p.name
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
