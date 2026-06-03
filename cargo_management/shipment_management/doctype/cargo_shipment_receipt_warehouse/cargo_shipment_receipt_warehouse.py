from frappe.model.document import Document


class CargoShipmentReceiptWarehouse(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		gross_weight: DF.Float
		height: DF.Float
		length: DF.Float
		package_type: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		transportation: DF.Literal["Sea", "Air"]
		warehouse_receipt: DF.Link
		weight: DF.Float
		width: DF.Float
	# end: auto-generated types

	pass
