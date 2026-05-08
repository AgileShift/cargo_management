from frappe.model.document import Document


class WarehouseReceiptLine(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		carrier_delivered_at: DF.Datetime | None
		carrier_weight: DF.Float
		customer: DF.Link | None
		customer_name: DF.ReadOnly | None
		height: DF.Float
		length: DF.Float
		parcel: DF.Link
		parcel_transportation: DF.Literal["Sea", "Air"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		type: DF.Literal["", "Box", "Envelope", "Pallet", "Mail"]
		warehouse_weight: DF.Float
		width: DF.Float
	# end: auto-generated types

	@property
	def volume(self):
		return self.length * self.width * self.height
