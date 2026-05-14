from frappe.model.document import Document


class CargoShipmentWarehouse(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		height: DF.Float
		length: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		reference: DF.Data | None
		transportation: DF.Literal["Sea", "Air"]
		type: DF.Data | None
		warehouse_receipt: DF.Link
		weight: DF.Float
		width: DF.Float
	# end: auto-generated types

	pass
