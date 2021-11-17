from frappe.model.document import Document


class CargoShipmentReceipt(Document):
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
