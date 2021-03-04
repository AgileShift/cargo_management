from frappe.model.document import Document
from frappe.model.utils.rename_doc import update_linked_doctypes, get_fetch_fields

class CargoShipmentReceipt(Document):

	def validate(self):
		# print(
		# 	sorted(self.cargo_shipment_receipt_lines, key=lambda item: item.customer_name)
		# )

		# for i, item in enumerate(sorted(self.cargo_shipment_receipt_lines, key=lambda item: item.customer), start=1):
		# 	item.idx = i

		super(CargoShipmentReceipt, self).validate()

	def before_save(self):
		

		super(CargoShipmentReceipt, self).before_save()

	# def on_update(self):
		""" After succesfull save. We link our docs! """

		# for csrl in self.cargo_shipment_receipt_lines:
		# 	print(csrl.customer)
		# 	update_linked_doctypes('Customer')
		#
		# super(CargoShipmentReceipt, self).on_update()
