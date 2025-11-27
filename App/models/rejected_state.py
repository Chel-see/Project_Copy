from App.models.application_state import ApplicationState
from App.models.shortlisted_state import ShortlistedState

class RejectedState(ApplicationState):
    def __init__(self, reason="Not specified"):
        super().__init__("Rejected")
        self.reason = reason

    def next(self):
        return None  # No next state from Rejected

    def previous(self):
        if self.context:
            self.context.setState(ShortlistedState())
        
    def viewReason(self):
        return self.reason

    def withdraw(self):
        return None  # Cannot withdraw a rejected application

    def getMatchedCompanies(self):
        return []  # No matched companies for rejected applications