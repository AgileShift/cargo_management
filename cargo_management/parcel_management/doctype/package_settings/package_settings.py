from frappe.model.document import Document


class PackageSettings(Document):

	def set_name_in_children(self):
		# Overrides and set a custom name for the child rows PackageCarrier. This cannot be done in the child Class.
		for doc in self.get_all_children():
			if not doc.name:
				doc.name = doc.carrier  # We keep on Sync
