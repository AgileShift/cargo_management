import frappe
from frappe.model.document import Document


class WarehouseReceiptQuickEntry(Document):
	pass


@frappe.whitelist(allow_guest=True)
def create_warehouse_receipt_line_from_quick_entry(quick_entry):
	# TODO: Get a way to configure where we will put new quick entry packages
	quick_entry = frappe.parse_json(quick_entry)

	lines = []
	for line in quick_entry.pieces:
		line = frappe.parse_json(line)
		lines.append({
			'package': quick_entry.tracking_number,
			'type': line.type,
			'customer': quick_entry.customer,
			'customer_name': quick_entry.customer_name,
			'carrier': quick_entry.carrier,
			'warehouse_description': quick_entry.warehouse_description,
			'customer_description': quick_entry.customer_description,
			'warehouse_est_weight': line.weight,
			'length': line.length,
			'width': line.width,
			'height': line.height,
			# TODO: Add Shipper Field
		})

	wr = frappe.get_doc({
		'doctype': 'Warehouse Receipt',
		'transportation': quick_entry.transportation,
		'notes': quick_entry.notes,
		'warehouse_receipt_lines': lines,

		# FIXME:
		'shipper': quick_entry.shipper,
		'consignee': quick_entry.customer_name
	}).insert(ignore_permissions=True, ignore_links=True)

	return wr
