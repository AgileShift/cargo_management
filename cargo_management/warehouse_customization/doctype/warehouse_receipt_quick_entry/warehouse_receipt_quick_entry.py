import frappe
from frappe.model.document import Document


class WarehouseReceiptQuickEntry(Document):
	pass


def create_warehouse_receipt_line_from_quick_entry(quick_entry):
	# TODO: Get a way to configure where we will put new quick entry packages

	wr = frappe.get_doc({
		'doctype': 'Warehouse Receipt',
		'transportation': '',
	})#.insert(ignore_permissions=True, ignore_links=True)

# Refactor Transportation Type o Transportation
