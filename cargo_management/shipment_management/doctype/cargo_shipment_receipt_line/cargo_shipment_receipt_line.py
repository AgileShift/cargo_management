from frappe.model.document import Document


class CargoShipmentReceiptLine(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		billable_qty_or_weight: DF.Float
		carrier_est_weight: DF.Float
		content: DF.Text | None
		customer: DF.Link | None
		customer_name: DF.Data | None
		gross_weight: DF.Float
		item_code: DF.Link | None
		item_price: DF.Currency
		package: DF.Link
		package_2: DF.ReadOnly | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		sales_invoice: DF.Link | None
		warehouse_receipt: DF.Link | None
	# end: auto-generated types
	pass
