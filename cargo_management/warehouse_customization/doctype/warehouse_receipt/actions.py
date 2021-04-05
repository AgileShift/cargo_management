import frappe


@frappe.whitelist()
def update_status(doc, new_status):
    doc = frappe.parse_json(doc)  # Getting the Warehouse Receipt Doc.

    docs_to_update = {
        'Package': {
            'new_status': new_status,
            'doc_names': doc.get('warehouse_receipt_lines')
        }
    }

    print(docs_to_update)



    # for i, wr_line in enumerate(doc.warehouse_receipt_lines, start=1):
    #     progress = i * 100 / len(doc.warehouse_receipt_lines)

        # TODO: Fix, after publish progress: CTL+S is not working.
        # frappe.publish_progress(
        #     percent=progress, title='Confirming Packages',
        #     description='Confirming Package {0}'.format(package.tracking_number),
        # )
#36 original
#16 lineas, despues de refactorizar
