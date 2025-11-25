from App.models import Shortlist, Position, Staff, Student, Application
from App.database import db

# 1. GET ELIGIBLE STUDENTS FOR A POSITION (GPA + Applied)
def get_eligible_students(position_id):

    position = Position.query.filter_by(id=position_id).first()
    if not position:
        return {"error": "Position not found"}, 404

    gpa_required = position.gpa_requirement

    # all applications for this position
    applications = Application.query.filter_by(position_id=position_id).all()

    eligible = []

    for app in applications:
        student = Student.query.filter_by(id=app.student_id).first()
        if not student:
            continue
        
        # GPA filter
        if gpa_required is None or student.gpa >= gpa_required:
            eligible.append({
                "student_id": student.id,
                "name": student.name,
                "gpa": student.gpa,
                "resume": student.resume,
                "status": app.status
            })

    return eligible, 200


# 2. GET ALL SHORTLISTS FOR A STUDENT
def get_shortlist_by_student(student_id):
    entries = Shortlist.query.filter_by(student_id=student_id).all()
    return [e.toJSON() for e in entries], 200


# 3. GET ALL SHORTLISTS FOR A POSITION
def get_shortlist_by_position(position_id):
    entries = Shortlist.query.filter_by(position_id=position_id).all()
    return [e.toJSON() for e in entries], 200


