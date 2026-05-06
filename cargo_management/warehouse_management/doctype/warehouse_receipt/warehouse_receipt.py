import frappe
from cargo_management.utils import get_list_from_child_table
from frappe.model.document import Document


class WarehouseReceipt(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cargo_management.warehouse_management.doctype.warehouse_receipt_line.warehouse_receipt_line import WarehouseReceiptLine
		from frappe.types import DF

		carrier_gross_weight: DF.Float
		date: DF.Date
		gross_weight: DF.Float
		status: DF.Literal["Open", "Awaiting Departure", "In Transit", "Sorting", "Finished"]
		total_volume: DF.Float
		transportation: DF.Literal["", "Sea", "Air"]
		warehouse: DF.Link
		warehouse_receipt_lines: DF.Table[WarehouseReceiptLine]
	# end: auto-generated types

	def validate(self):

		self.gross_weight = 0
		self.carrier_gross_weight = 0

		for row in self.warehouse_receipt_lines:
			self.gross_weight += row.warehouse_weight or 0.00
			self.carrier_gross_weight += row.carrier_weight or 0.00

	def on_update(self):
		""" Add Warehouse Receipt Link to the Package. This allows to have mutual reference WR to Package. """
		# FIXME: If Warehouse Receipt is deleted, remove link from Package
		# TODO: Add extra fields from Warehouse Receipt -> Receipt Date & Weight

		# We only change the warehouse_receipt field if it is different from the current
		parcels = get_list_from_child_table(self.warehouse_receipt_lines, 'parcel')

		if not parcels:
			return

		# TODO: Improve
		frappe.db.sql("""
					  UPDATE tabParcel SET warehouse_receipt = %(wr_name)s
					  WHERE name IN %(parcels)s AND COALESCE(warehouse_receipt, '') != %(wr_name)s
		""", {
			'wr_name': self.name,
			'parcels': parcels
		})

	# TODO: Actually change the status after the parcel is validated and created. maybe at status change from draft to open?

	def change_status(self, new_status):
		""" Validates the current status of the warehouse receipt and change it if it's possible. """

		# TODO: Validate this when status is changed on Form-View or List-View

		# TODO: FINISH
		if self.status != new_status and \
			(self.status == 'Open' and new_status == 'Awaiting Departure') or \
			(self.status in ['Open', 'Awaiting Departure'] and new_status == 'In Transit') or \
			(self.status in ['Open', 'Awaiting Departure', 'In Transit'] and new_status == 'Sorting') or \
			(self.status in ['Open', 'Awaiting Departure', 'In Transit', 'Sorting'] and new_status == 'Finished'):
			self.status = new_status
			return True

		return False
