from collections import defaultdict

import frappe
from cargo_management.utils import get_list_from_child_table, update_status_in_bulk


@frappe.whitelist(methods='POST')
def update_status(source_doc_name: str, new_status: str):
    doc = frappe.get_cached_doc('Cargo Shipment Receipt', source_doc_name)  # Getting the Cargo Shipment Receipt Doc

    # HOTFIX
    cargo_shipment = frappe.get_doc('Cargo Shipment', doc.cargo_shipment)

    # We Mark the actual child tables added to the parent, because we can dynamically add
    update_status_in_bulk(docs_to_update={
        'Cargo Shipment Receipt': [doc.name],
        'Cargo Shipment': [doc.cargo_shipment],
        'Warehouse Receipt': get_list_from_child_table(cargo_shipment.cargo_shipment_lines, 'warehouse_receipt'),
        'Parcel': get_list_from_child_table(doc.cargo_shipment_receipt_lines, 'package')
    }, new_status=new_status, msg_title='Marked as Sorting', mute_emails=doc.mute_emails)


@frappe.whitelist(methods='POST')
def make_sales_invoice(doc):
    # TODO: Que se guarde el invoice en cada uno, para que no se repita la creacion de cada factura, en cada intento
    # TODO: Set customer if not set!

    """ Create a sales invoice for each customer with items as packages. From Cargo Shipment Receipt """
    doc = frappe.parse_json(doc)
    cargo_shipment_receipt = frappe.get_doc('Cargo Shipment Receipt', doc.get('name'))

    # Sorting all the customers data in a single dict
    customers_to_invoice = defaultdict(list)
    warning_messages = []
    for item in cargo_shipment_receipt.cargo_shipment_receipt_lines:
        if not item.customer:
            frappe.throw('Agregar cliente a fila: {}, Paquete: {}'.format(item.get('idx'), item.get('package')))

        if item.sales_invoice:
            # TODO: What happens if invoice exists and there is a new sales item?
            warning_messages.append('No se creara factura para: {}. Ya tiene Factura.'.format(item.get('package')))
            continue

        customers_to_invoice[item.customer].append(item)

    # print('warning_messages')
    # frappe.msgprint(msg=warning_messages, title='Advertencias', as_list=True, indicator='orange')

    # if not customers_to_invoice:
    #     return None

    # Creating a Sales Invoice for each customer
    # TODO: Validate fields and throw before start to create sales order!
    for customer in customers_to_invoice:
        sales_invoice = frappe.new_doc('Sales Invoice')
        sales_invoice.customer = customer  # Company and Currency are automatically set

        # Iterate over customer items to invoice
        # csrl_invoiced_items = []
        for item in customers_to_invoice[customer]:
            item_data = {  # Always pass this data
                'item_code': item.item_code,
                'package': item.package,
                'qty': item.billable_qty_or_weight or item.gross_weight,  # TODO: Rename billable_qty_or_weight
                'weight_per_unit': item.gross_weight if item.billable_qty_or_weight else 1,
                'total_weight': item.gross_weight,
                'description': item.content or item.item_code
            }

            # if item.item_price > 0.00:
            #     item_data.update({'price_list_rate': item.item_price}) # TODO: Remove this field?

            sales_invoice.append('items', item_data)  # Add each items
            # csrl_invoiced_items.append(item.name)

        print('Before Saving?')

        sales_invoice.set_missing_values()
        sales_invoice.save(ignore_permissions=True)  # Saving a invoice as draft

        print('creating sales invoice?')

        # for item in csrl_invoiced_items:
        #     print(item, sales_invoice.name)
        #     frappe.db.set_value('Cargo Shipment Receipt Line', item, 'sales_invoice', sales_invoice.name, update_modified=False)
        #     frappe.db.commit()  # TODO: Not the best way. but its working

    # frappe.db.commit()  # Save all?

    # cargo_shipment_receipt.notify_update()
    # cargo_shipment_receipt.save(ignore_permissions=True)  # Send update notify

    # TODO: Work in Progress
    update_status_in_bulk(docs_to_update={
        'Cargo Shipment Receipt': {'doc_names': [cargo_shipment_receipt.name], 'new_status': 'Finished'},
        'Cargo Shipment': {'doc_names': [cargo_shipment_receipt.cargo_shipment], 'new_status': 'Finished'},
        # 'Warehouse Receipt': {'doc_names': get_list_from_child_table(cargo_shipment_receipt.cargo_shipment_receipt_warehouse_lines, 'warehouse_receipt'), 'new_status': 'Finished'},
        'Parcel': get_list_from_child_table(doc.cargo_shipment_receipt_lines, 'package')
    }, new_status='To Bill', msg_title='Updating Packages', mute_emails=doc.mute_emails)

    return customers_to_invoice  # TODO: Return the new sales invoice and update the cargo shipment table?
