import frappe
from frappe.model.document import Document


class CargoShipment(Document):
	"""
		TODO: Enable Doctype Quick Entry
		If doctype "Quick Entry" and field "date" default value: "Now" its fails miserably:
		https://github.com/frappe/frappe/issues/11001
	"""

	def before_save(self):

		for cargo_shipment_line in self.cargo_shipment_lines:
			# FIXME: A better way to handle this?
			frappe.db.set_value('Warehouse Receipt', cargo_shipment_line.warehouse_receipt, 'departure_date', self.departure_date, update_modified=False)

