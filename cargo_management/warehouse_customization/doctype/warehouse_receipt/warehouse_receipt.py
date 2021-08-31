import frappe
from cargo_management.utils import get_list_from_child_table
from frappe.model.document import Document


class WarehouseReceipt(Document):

    def on_update(self):
        """ Add Warehouse Receipt Link to the Package. This allow to have mutual reference WR to Package. """
        # FIXME: If Warehouse Receipt is deleted, remove link from Package
        # TODO: Add extra fields from Warehouse Receipt -> Receipt Date & Weight

        # We only set the warehouse_receipt if it is different
        frappe.db.sql("""
            UPDATE tabPackage
            SET warehouse_receipt = %(wr_name)s
            WHERE warehouse_receipt != %(wr_name)s AND `name` IN %(packages)s
        """, {
            'wr_name': self.name,
            'packages': get_list_from_child_table(self.warehouse_receipt_lines, 'package')
        })

    def change_status(self, new_status):
        """ Validates the current status of the warehouse receipt and change it if it's possible. """
        # TODO: Validate this when status is changed on Form-View or List-View

        # TODO: FINISH
        if self.status != new_status and \
                (self.status == 'Awaiting Departure' and new_status == 'In Transit') or \
                (self.status in ['Awaiting Departure', 'In Transit'] and new_status == 'Sorting') or \
                (self.status in ['Awaiting Departure', 'In Transit', 'Sorting'] and new_status == 'Finished'):
            self.status = new_status
            return True

        return False
