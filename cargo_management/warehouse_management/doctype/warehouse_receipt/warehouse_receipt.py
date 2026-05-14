import frappe
from cargo_management.utils import pluck_child_field
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
		height: DF.Float
		length: DF.Float
		manual_weight: DF.Check
		status: DF.Literal["Open", "Awaiting Departure", "In Transit", "Sorting", "Finished"]
		total_volume: DF.Float
		transportation: DF.Literal["", "Sea", "Air"]
		type: DF.Literal["", "Box", "Envelope", "Bag", "Tube", "EH Container", "Parcel Bag(Sack)", "Pallet"]
		warehouse: DF.Link
		warehouse_receipt_lines: DF.Table[WarehouseReceiptLine]
		width: DF.Float
	# end: auto-generated types

	def validate(self):

		if self.manual_weight:
			return

		self.gross_weight = 0
		self.carrier_gross_weight = 0

		for row in self.warehouse_receipt_lines:
			self.gross_weight += row.warehouse_weight or 0.00
			self.carrier_gross_weight += row.carrier_weight or 0.00

	def on_update(self):
		""" Add Warehouse Receipt Link to the Parcel """
		# FIXME: If Warehouse Receipt is deleted, remove link from Parcel
		# TODO: Add extra fields from Warehouse Receipt -> Receipt Date & Weight
		# TODO: Change the warehouse_receipt field on Parcel only if it is different

		parcel_names = pluck_child_field(self.warehouse_receipt_lines, 'parcel')

		if not parcel_names:
			return

		parcel = frappe.qb.DocType('Parcel')
		(
			frappe.qb.update(parcel)
			.set(parcel.warehouse_receipt, self.name)
			.where(parcel.name.isin(parcel_names))
			.where(
				parcel.warehouse_receipt.isnull() | parcel.warehouse_receipt != self.name
			)
		).run()

	def change_status(self, new_status):
		""" Validates the current status of the warehouse receipt and change it if it's possible. """
		# TODO: Change the status after the parcel is created and validated. maybe at status change from draft to open?
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
# 87 Working on the Link Motor
