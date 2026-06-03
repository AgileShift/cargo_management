from cargo_management.engine import LinkSyncMixin, LinkSyncRule
from frappe.model.document import Document


class CargoShipmentReceipt(Document, LinkSyncMixin):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cargo_management.shipment_management.doctype.cargo_shipment_receipt_line.cargo_shipment_receipt_line import CargoShipmentReceiptLine
		from cargo_management.shipment_management.doctype.cargo_shipment_receipt_warehouse.cargo_shipment_receipt_warehouse import CargoShipmentReceiptWarehouse
		from frappe.types import DF

		arrival_date: DF.Date
		cargo_shipment: DF.Link
		cargo_shipment_receipt_lines: DF.Table[CargoShipmentReceiptLine]
		cargo_shipment_receipt_warehouse: DF.Table[CargoShipmentReceiptWarehouse]
		departure_date: DF.Date | None
		gross_weight: DF.Float
		status: DF.Literal["Awaiting Receipt", "Sorting", "Finished"]
		transportation: DF.Literal["", "Sea", "Air"]
	# end: auto-generated types

	link_sync_rules = (
		# TODO, Add the cargo_shipment_receipt field on the Cargo Shipment
		LinkSyncRule("cargo_shipment_receipt_warehouse", "warehouse_receipt", "Warehouse Receipt", "cargo_shipment_receipt"),
		LinkSyncRule("cargo_shipment_receipt_lines", "parcel", "Parcel", "cargo_shipment_receipt"),
	)

	# TODO: Set customer on update!
	def before_validate(self):
		self.gross_weight = 0
		for parcel in self.cargo_shipment_receipt_lines:
			self.gross_weight += parcel.gross_weight or 0.00
		self.validate_link_sync()

	def before_save(self):
		self.capture_link_sync_state()

	def on_update(self):
		self.sync_links()

	def on_trash(self):
		self.unlink_synced_links()

	def validate(self):
		# TODO: make this sort function refresh the table
		sorted_list = sorted(
			self.cargo_shipment_receipt_lines,
			key=lambda parcel: (
				parcel.customer_name if parcel.customer_name else '',
				-float(parcel.gross_weight) if parcel.gross_weight else 0.00
			)
		)
		for i, parcel in enumerate(sorted_list, start=1):
			parcel.idx = i

	def change_status(self, new_status):
		""" Validates the current status of the cargo shipment receipt and change it if it's possible. """
		# TODO: Validate this when status is changed on Form-View or List-View

		# TODO: Finish
		if self.status != new_status and \
				(self.status == 'Awaiting Receipt' and new_status == 'Sorting') or \
				(self.status == 'Sorting' and new_status == 'Finished'):
			self.status = new_status
			return True

		return False
