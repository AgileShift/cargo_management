# -*- coding: utf-8 -*-
# Copyright (c) 2020, Agile Shift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document


class ParcelCarrier(Document):

	"""
	# TODO:
	We choose this Doctype to act as a child to ParcelSettings and a Link for Parcel.

	Field:
	carrier_name: Is the readable carrier name for the customer
	carrier_code: Is the code chosen by the external API

	name is set to: field:carrier_code

	On any case, we change the carrier_code from the ParcelSettings, the name field is not "renamed".
	Causing multiple discrepancies eg:
		carrier_code works with the API but the Parcel has a Link to an outdated code.

	Solution is to change the carrier_code from the ParcelSettings and also rename:
		http://localhost/desk#Form/Parcel%20Carrier/{name}
		Here we can rename the field selected as name(carrier_code), and the frappe name id key.

	Workaround: When carrier_code is changed, automatically rename the name id field.
	"""

	pass
