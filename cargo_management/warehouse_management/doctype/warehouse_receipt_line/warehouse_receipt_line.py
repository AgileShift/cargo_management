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
		package_type: DF.Literal["", "Box", "Envelope", "Bag", "Tube", "Pallet"]
		parcel: DF.Link
		parcel_transportation: DF.Literal["", "Sea", "Air"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		warehouse_weight: DF.Float
		width: DF.Float
	# end: auto-generated types

	@property
	def volume_cuft(self):
		if not self.length or not self.width or not self.height:
			return 0
		return (self.length * self.width * self.height) / 1728
