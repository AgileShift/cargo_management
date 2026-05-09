from frappe.model.document import Document


class CarrierTrackingURL(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		label: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		type: DF.Literal["Official", "Alternative", "Fallback", "Internal"]
		url: DF.Data
	# end: auto-generated types

	pass
