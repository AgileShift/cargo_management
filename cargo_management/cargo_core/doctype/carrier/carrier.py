import frappe
from frappe.model.document import Document


class Carrier(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cargo_management.cargo_core.doctype.carrier_tracking_url.carrier_tracking_url import CarrierTrackingURL
		from frappe.types import DF

		api: DF.Literal["", "17Track", "AfterShip", "EasyPost"]
		regex: DF.Code | None
		regex_notes: DF.MarkdownEditor | None
		tracking_urls: DF.Table[CarrierTrackingURL]
	# end: auto-generated types

	def validate(self):
		if self.regex:  # Test if the regex is valid
			import re
			try:
				re.compile(self.regex)
			except re.error:
				frappe.throw(f"Invalid regex pattern: {self.regex}")
