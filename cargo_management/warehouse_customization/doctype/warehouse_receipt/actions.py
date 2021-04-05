import frappe


def confirm_packages_in_wr(doc):
    package = doc

    for i, wr_line in enumerate(doc.warehouse_receipt_lines, start=1):
        progress = i * 100 / len(doc.warehouse_receipt_lines)

        # TODO: Fix, after publish progress: CTL+S is not working.
        frappe.publish_progress(
            percent=progress, title='Confirming Packages',
            description='Confirming Package {0}'.format(package.tracking_number),
        )
#36