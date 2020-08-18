# -*- coding: utf-8 -*-
# Copyright (c) 2020, Agile Shift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document


class WarehouseReceipt(Document):
	# TODO: Pieces must be the sum of what:
	# Total pieces on warehouse in warehouse receipt
	# total pieces on each package in warehouse receipt
	# total pieces after packing?
	pass
