from cargo_management.engine import LinkSyncMixin, LinkSyncRule
from cargo_management.engine.utils import pluck_child_field
from frappe.model.document import Document


CBM_PER_CUFT = 0.028316846592


class WarehouseReceipt(Document, LinkSyncMixin):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cargo_management.warehouse_management.doctype.warehouse_receipt_line.warehouse_receipt_line import WarehouseReceiptLine
		from frappe.types import DF

		cargo_shipment: DF.Link | None
		cargo_shipment_receipt: DF.Link | None
		date: DF.Date
		height: DF.Float
		length: DF.Float
		manual_weight: DF.Check
		status: DF.Literal["Open", "Awaiting Departure", "In Transit", "Sorting", "Finished"]
		total_carrier_weight: DF.Float
		total_parcels: DF.Int
		total_pieces: DF.Int
		total_warehouse_weight: DF.Float
		transportation: DF.Literal["", "Sea", "Air"]
		type: DF.Literal["", "Loose", "Box", "Envelope", "Bag", "Tube", "EH Container", "Parcel Bag(Sack)", "Pallet"]
		warehouse: DF.Link
		warehouse_receipt_lines: DF.Table[WarehouseReceiptLine]
		width: DF.Float
	# end: auto-generated types

	link_sync_rules = (
		LinkSyncRule("warehouse_receipt_lines", "parcel", "Parcel", "warehouse_receipt"),
	)

	def before_validate(self):
		self._apply_requested_single_line_defaults()
		total_warehouse_weight, self.total_carrier_weight = 0, 0

		for row in self.warehouse_receipt_lines:
			total_warehouse_weight += row.warehouse_weight
			self.total_carrier_weight += row.carrier_weight

		if not self.manual_weight:
			self.total_warehouse_weight = total_warehouse_weight

		self.total_parcels = len(set(pluck_child_field(self.warehouse_receipt_lines, "parcel")))
		self.validate_link_sync()

	def before_save(self):
		self.capture_link_sync_state()

	def on_update(self):
		self.sync_links()

	def on_trash(self):
		self.unlink_synced_links()

	@property
	def total_volume_cuft(self):
		return sum(row.volume_cuft for row in self.warehouse_receipt_lines) or self._calculate_volume_cuft(
			self.length,
			self.width,
			self.height,
		)

	@property
	def total_volume_cbm(self):
		return self.total_volume_cuft * CBM_PER_CUFT

	def _apply_requested_single_line_defaults(self):
		if not self.get("copy_single_line_details"):
			return

		if len(self.warehouse_receipt_lines) == 1:
			self._apply_single_line_defaults()

		self.copy_single_line_details = 0

	@staticmethod
	def _calculate_volume_cuft(length: float, width: float, height: float) -> float:
		if not length or not width or not height:
			return 0

		return (length * width * height) / 1728

	def _apply_single_line_defaults(self):
		""" Set the defaults for single line warehouse receipts """
		row = self.warehouse_receipt_lines[0]

		self.type = row.package_type
		self.length = row.length
		self.width = row.width
		self.height = row.height

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
