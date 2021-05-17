from frappe.model.document import Document
import frappe


class WarehouseReceipt(Document):
    # TODO: Finalizar el peso por volumen y peso reportado de cada paquete
    # TODO: Finalizar el peso por volumen y peso reportado global

    # TODO: Pieces -> SUM of pieces of each package in warehouse receipt?
    # TODO: Weight -> SUM of weight of each package in warehouse receipt?
    """
        TODO: Enable Doctype Quick Entry for Opening Date as now
        If doctype "Quick Entry" and field "date" default value: "Now" its fails miserably:
        https://github.com/frappe/frappe/issues/11001
    """

    def on_update(self):
        """ Add the Warehouse Receipt to the Package Doc. This allow to have mutual reference WR to Pack """
        # TODO: Set only if is not set  ?
        # TODO: What happens if deleted - It must be some sort of cleaning method? ?

        for wr_line in self.warehouse_receipt_lines:
            # TODO: Add: Warehouse -> Receipt Date & Weight
            frappe.db.set_value('Package', wr_line.get('package'), 'warehouse_receipt', self.name, update_modified=False)

    def change_status(self, new_status):
        """ Validates the current status of the warehouse receipt and change it if it's possible. """
        # TODO: Validate this when status is changed on Form-View or List-View

        if self.status != new_status and \
                (self.status == 'Awaiting Departure' and new_status == 'In Transit') or \
                (self.status in ['Awaiting Departure', 'In Transit'] and new_status == 'Sorting') or \
                (self.status in ['Awaiting Departure', 'In Transit', 'Sorting'] and new_status == 'Finished'):
            # TODO: Finish
            print('TRUE . From {0}, To {1}: {2}'.format(self.status, new_status, self.reference))

            self.status = new_status
            return True

        print('FALSE. Is {} was going to {}: {}'.format(self.status, new_status, self.reference))
        return False
