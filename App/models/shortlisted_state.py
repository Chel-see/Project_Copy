from App.models.application_state import ApplicationState

class ShortListedState(ApplicationState):
    def __init__(self):
        super().__init__("Shortlisted")

    # Shortlisted → requires decision (no automatic next)
    def next(self, app, decision=None):
        if decision is None:
            return None

        if decision == "accept":
            from App.models.accepted_state import AcceptedState
            app.set_state(AcceptedState())

        elif decision == "reject":
            from App.models.rejected_state import RejectedState
            app.set_state(RejectedState())
    
    # Shortlisted → Applied
    def previous(self, app):
        from App.models.applied_state import AppliedState
        app.set_state(AppliedState())

    def withdraw(self, app):
        # Student withdraws: move to rejected
        from App.models.rejected_state import RejectedState
        app.set_state(RejectedState())

    def getMatchedCompanies(self, app):
        """Return all Shortlisted applications for the same student."""
        from App.models.application import Application

        # We cannot rely on old 'context', now we use the app argument
        student_id = app.student_id

        shortlisted = Application.query.filter_by(
            student_id=student_id,
            status="Shortlisted"
        ).all()

        return [repr(a) for a in shortlisted]

















# from App.models.application_state import ApplicationState

# class ShortListedState(ApplicationState):
#     def __init__(self):
#         super().__init__("Shortlisted")

#     def next(self): # No automatic nect state, next state requires decision (parameter)
#         return None
    
#     def next_decision(self, app,decision: str): #Accepts decision from make_decision() in employer controller
#         if decision == "accept":
#             from App.models.accepted_state import AcceptedState
#             app.set_state(AcceptedState())
#         elif decision == "reject":
#             from App.models.rejected_state import RejectedState
#             app.set_state(RejectedState())

#     def previous(self,app):
       
#             from App.models.applied_state import AppliedState
#             app.set_state(AppliedState())

#     def removeShortList(self):
#         return None #Not implemented - to be removed

#     def withdraw(self, app):
#         from App.models.rejected_state import RejectedState
#         app.set_state(RejectedState())

#     def getMatchedCompanies(self,app):
#         from App.models.application import Application
#         if not self.context or not self.context.application:
#             return []
#         student_id = self.context.application.student_id
#         #Applications that are in shortlisted state
#         shortlisted_pos = Application.query.filter_by(student_id=student_id, status="Shortlisted").all()
#         return [app.__repr__() for app in shortlisted_pos]
