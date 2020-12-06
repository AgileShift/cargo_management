from frappe.model.document import Document


class WarehouseReceipt(Document):
	# TODO: Pieces -> SUM of pieces of each parcel in warehouse receipt?
	# TODO: Weight -> SUM of weight of each parcel in warehouse receipt?
	"""
		TODO: Enable Doctype Quick Entry
		If doctype "Quick Entry" and field "date" default value: "Now" its fails miserably:
		https://github.com/frappe/frappe/issues/11001
	"""
	pass
