from App.models.application_state import ApplicationState

class ShortListedState(ApplicationState):
    def __init__(self):
        super().__init__("Shortlisted")

    def next(self): # No automatic nect state, next state requires decision (parameter)
        return None
    
    def next_decision(self, decision: str): #Accepts decision from make_decision() in employer controller
        if decision == "accept":
            from App.models.accepted_state import AcceptedState
            self.context.setState(AcceptedState())
        elif decision == "reject":
            from App.models.rejected_state import RejectedState
            self.context.setState(RejectedState())

    def previous(self):
        if self.context:
            from App.models.applied_state import AppliedState
            self.context.setState(AppliedState())

    def removeShortList(self):
        return None #Not implemented - to be removed

    def withdraw(self):
        from App.models.rejected_state import RejectedState
        self.context.setState(RejectedState())

    def getMatchedCompanies(self):
        from App.models.application import Application
        if not self.context or not self.context.application:
            return []
        student_id = self.context.application.student_id
        #Applications that are in shortlisted state
        shortlisted_pos = Application.query.filter_by(student_id=student_id, status="Shortlisted").all()
        return [app.__repr__() for app in shortlisted_pos]
