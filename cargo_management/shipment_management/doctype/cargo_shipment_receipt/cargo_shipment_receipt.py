from frappe.model.document import Document


class CargoShipmentReceipt(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cargo_management.shipment_management.doctype.cargo_shipment_receipt_line.cargo_shipment_receipt_line import CargoShipmentReceiptLine
		from frappe.types import DF

		arrival_date: DF.Date | None
		cargo_shipment: DF.Link
		cargo_shipment_receipt_lines: DF.Table[CargoShipmentReceiptLine]
		departure_date: DF.Date | None
		gross_weight: DF.Float
		mute_emails: DF.Check
		status: DF.Literal['Awaiting Receipt', 'Sorting', 'Finished']
	# end: auto-generated types

	# TODO: Set customer on update!

	def validate(self):
		# TODO: make this sort function refresh the table
		sorted_list = sorted(self.cargo_shipment_receipt_lines, key=lambda item: item.customer_name if item.customer_name else '')
		for i, item in enumerate(sorted_list, start=1):
			item.idx = i

	def change_status(self, new_status):
		""" Validates the current status of the cargo shipment receipt and change it if it's possible. """
		# TODO: Validate this when status is changed on Form-View or List-View

		# TODO: Finish
		if self.status != new_status and \
				(self.status == 'Awaiting Receipt' and new_status == 'Sorting') or \
				(self.status == 'Sorting' and new_status =='Finished'):
			self.status = new_status
			return True

		return False
