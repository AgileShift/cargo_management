from frappe.model.document import Document


class CargoPackingListLine(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		consignee: DF.Data | None
		customer_description: DF.SmallText | None
		package: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		total: DF.Currency
		warehouse_description: DF.SmallText | None
		wr_reference: DF.Data | None
	# end: auto-generated types

	pass
