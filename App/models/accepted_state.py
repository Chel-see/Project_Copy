from models.application_state import ApplicationState


class AcceptedState(ApplicationState):
    def __init__(self):
        super().__init__("Accepted")

    def next(self):
        return None  # No direct next state from Accepted

    def previous(self):
        if self.context:
            from models.shortlisted_state import ShortListedState
            self.context.setState(ShortListedState())  # No previous state from Accepted

    def acceptOffer(self):
        self.name="Confirmed"

    def withdraw(self):
        if self.context: # check if there is a valid context
            from models.rejected_state import RejectedState
            self.context.setState(RejectedState())
            
    def getMatchedCompanies(self):
        return []  # No matched companies for accepted applications
