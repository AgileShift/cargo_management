from frappe.model.document import Document


class CargoShipmentLine(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		carrier: DF.Link | None
		carrier_est_weight: DF.Float
		carrier_real_delivery: DF.Datetime | None
		customer: DF.Link | None
		customer_name: DF.Data | None
		description: DF.SmallText | None
		height: DF.Float
		length: DF.Float
		parcel: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		received_date: DF.Date | None
		transportation: DF.Literal["Sea", "Air"]
		type: DF.Literal["Box", "Envelope", "Pallet"]
		volumetric_weight: DF.Float
		warehouse_est_weight: DF.Float
		warehouse_receipt: DF.Link | None
		width: DF.Float
	# end: auto-generated types

	pass
