from frappe.model.document import Document


class CargoShipmentWarehouse(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		reference: DF.Data
		warehouse_receipt: DF.Link
		weight: DF.Float
	# end: auto-generated types

	pass
