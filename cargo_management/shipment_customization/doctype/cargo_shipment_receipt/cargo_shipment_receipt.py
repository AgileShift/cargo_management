from frappe.model.document import Document
from frappe.model.utils.rename_doc import update_linked_doctypes, get_fetch_fields

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
