from frappe.model.document import Document


class WarehouseReceipt(Document):
	# TODO: Pieces -> SUM of pieces of each package in warehouse receipt?
	# TODO: Weight -> SUM of weight of each package in warehouse receipt?
	"""
		TODO: Enable Doctype Quick Entry for Opening Date as now
		If doctype "Quick Entry" and field "date" default value: "Now" its fails miserably:
		https://github.com/frappe/frappe/issues/11001
	"""
	def change_status(self, new_status):
		""" Validates the current status of the wharehouse receipt and change it if it's possible. """
		# TODO: Validate this when status is changed on Form-View or List-View

		if self.status != new_status and \
				(self.status == 'Awaiting Departure' and new_status == 'In Transit') or \
				(self.status in ['Awaiting Departure', 'In Transit'] and new_status == 'Sorting'):
			# TODO: Finish
			print('TRUE . From {0}, To {1}: {2}'.format(self.status, new_status, self.reference))

			self.status = new_status
			return True

		print('FALSE. Is {} was going to {}: {}'.format(self.status, new_status, self.reference))
		return False
