from .constants import Status
class ParcelStateMachine:
    def __init__(self, status = Status.AWAITING_RECEIPT):
        self.state = status


    def _allowed_transition(self, value, allowed_statuses: any) -> bool:
        if value in allowed_statuses:
            self.state = value
            return True
        else:
            return False
    

    def transition(self, event: Status) -> bool:
        match self.state:
            case Status.AWAITING_RECEIPT:
                return self._allowed_transition(event, [Status.AWAITING_CONFIRMATION, Status.RETURNED_TO_SENDER, Status.AWAITING_DEPARTURE, Status.SORTING])
            case Status.AWAITING_CONFIRMATION:
                return self._allowed_transition(event, [Status.AWAITING_DEPARTURE, Status.SORTING])
            case Status.IN_EXTRAORDINARY_CONFIRMATION:
                return self._allowed_transition(event, [Status.AWAITING_DEPARTURE, Status.SORTING])
            case Status.AWAITING_DEPARTURE:
                return self._allowed_transition(event, [Status.IN_TRANSIT, Status.SORTING])
            case Status.IN_TRANSIT:
                return self._allowed_transition(event, [Status.SORTING])
            case Status.FOR_DELIVERY_OR_PICKUP:
                return self._allowed_transition(event, [Status.TO_BILL])
            case Status.FINISHED:
                return self._allowed_transition(event, [Status.TO_BILL])
            case Status.TO_BILL:
                return self._allowed_transition(event, [Status.TO_BILL])
            case _:
                return False
                