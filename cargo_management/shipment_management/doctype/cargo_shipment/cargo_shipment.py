from cargo_management.engine import LinkSyncMixin, LinkSyncRule
from frappe.model.document import Document


class CargoShipment(Document, LinkSyncMixin):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cargo_management.shipment_management.doctype.cargo_shipment_line.cargo_shipment_line import CargoShipmentLine
		from cargo_management.shipment_management.doctype.cargo_shipment_warehouse.cargo_shipment_warehouse import CargoShipmentWarehouse
		from frappe.types import DF

		arrival_date: DF.Date | None
		cargo_shipment_lines: DF.Table[CargoShipmentLine]
		departure_date: DF.Date
		estimated_gross_weight_by_carriers_in_pounds: DF.Float
		estimated_gross_weight_by_warehouse_in_pounds: DF.Float
		expected_arrival_date: DF.Date
		pieces: DF.Int
		status: DF.Literal["Awaiting Departure", "In Transit", "Sorting", "Finished"]
		transportation: DF.Literal["", "Sea", "Air"]
		warehouse_lines: DF.Table[CargoShipmentWarehouse]
	# end: auto-generated types

	link_sync_rules = (
		LinkSyncRule("cargo_shipment_lines", "parcel", "Parcel", "cargo_shipment"),
	)

	def before_validate(self):
		self.validate_link_sync()

	def before_save(self):
		self.capture_link_sync_state()

	def on_update(self):
		# TODO: Add Departure Date to all Warehouse Receipt Linked
		self.sync_links()

	def on_trash(self):
		self.unlink_synced_links()

	def change_status(self, new_status):
		""" Validates the current status of the cargo shipment and change it if it's possible. """
		# TODO: Validate this when status is changed on Form-View or List-View

		# TODO: Finish
		if self.status != new_status and \
			(self.status == 'Awaiting Departure' and new_status == 'In Transit') or \
			(self.status in ['Awaiting Departure', 'In Transit'] and new_status == 'Sorting') or \
			(self.status == 'Sorting' and new_status == 'Finished'):
			self.status = new_status
			return True

		return False
