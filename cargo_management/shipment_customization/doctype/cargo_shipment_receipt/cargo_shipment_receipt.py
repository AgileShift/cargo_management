from frappe.model.document import Document


class CargoShipmentReceipt(Document):

	def validate(self):
		# TODO: make this sort function refresh the table
		sorted_list = sorted(self.cargo_shipment_receipt_lines, key=lambda item: item.customer_name if item.customer_name else '')
		for i, item in enumerate(sorted_list, start=1 ):
			item.idx = i

	# def on_update(self):
		""" After succesfull save. We link our docs! """

		# for csrl in self.cargo_shipment_receipt_lines:
		# 	print(csrl.customer)
		# 	update_linked_doctypes('Customer')
		#
		# super(CargoShipmentReceipt, self).on_update()

	def change_status(self, new_status):
		""" Validates the current status of the cargo shipment receipt and change it if it's possible. """
		# TODO: Validate this when status is changed on Form-View or List-View

		if self.status != new_status and \
				self.status == 'Awaiting Receipt' and new_status == 'Sorting':
			# TODO: Finish
			print('TRUE . From {0}, To {1}: {2}'.format(self.status, new_status, self.reference))

			self.status = new_status
			return True

		print('FALSE. Is {} was going to {}: {}'.format(self.status, new_status, self.reference))
		return False
