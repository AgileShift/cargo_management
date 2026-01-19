from frappe.model.document import Document


class Carrier(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cargo_management.cargo_core.doctype.carrier_tracking_url.carrier_tracking_url import CarrierTrackingURL
		from frappe.types import DF

		api: DF.Literal["", "17Track", "EasyPost"]
		tracking_urls: DF.Table[CarrierTrackingURL]
	# end: auto-generated types

	pass
