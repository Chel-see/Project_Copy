from App.models import Shortlist, Position, Staff, Student, Application
from App.database import db


# 1. GET ELIGIBLE STUDENTS FOR A POSITION
def get_eligible_students(position_id):

    position = Position.query.filter_by(id=position_id).first()
    if not position:
        print("Position not found.")
        return None

    gpa_required = position.gpa_requirement

    # All existing Application entries for this position
    applications = Application.query.filter_by(position_id=position_id).all() # why not append all the students who have applications for this positions 
                                                                                #bc we already checked their gpa upon creation ?
    if not applications:
        print("No applications found for this position.")
        return []

    eligible_students = []

    for app in applications:
        student = Student.query.filter_by(id=app.student_id).first()
        if not student:
            continue

        # GPA filter
        if gpa_required is None or student.gpa >= gpa_required:
            eligible_students.append(student)

    return eligible_students


# 2. GET ALL SHORTLISTS FOR A STUDENT
def get_shortlist_by_student(student_id):

 

    return Application.query.filter(Application.student_id == student_id,Application.status == "Shortlisted").all()

    # shortlists = Shortlist.query.filter_by(student_id=student_id).all()
    # if not shortlists:
    #     print("No shortlist entries found for this student.")
    #     return []



# 3. GET ALL SHORTLISTS FOR A POSITION
def get_shortlist_by_position(position_id):

    position = Position.query.filter_by(id=position_id).first()
    if not position:
        print("Position not found.")
        return []
        
    return Shortlist.query.filter_by(position_id=position_id).all()
   

# 4. WITHDRAW A SHORTLIST ENTRY
def withdraw_shortlist(shortlist_id):

    shortlist = Shortlist.query.get(shortlist_id)

    if not shortlist:
        print("Shortlist entry not found.")
        return None

    # Already withdrawn → idempotent behavior
    if shortlist.checkWithdrawn():
        print("Shortlist already withdrawn — no action taken.")
        return shortlist

    # If the shortlist was accepted already, withdrawing is not allowed
    if shortlist.application.getStatus() == "Accepted" or shortlist.application.getStatus() == "Rejected": # look out for case sensitivity
        print("Cannot withdraw an accepted application.")
        return None
 
    shortlist.isWithdrawn = True
    shortlist.application.withdraw()

    # Update state machine
    db.session.commit()
    return shortlist


