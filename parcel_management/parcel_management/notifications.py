import frappe


@frappe.whitelist()
def get_notification_config():
    # TODO: Make this!
    return {
        "for_doctype": {
            "Package": {
                "status": "finished"
            },
        },
    }
