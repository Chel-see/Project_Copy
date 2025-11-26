# App/controllers/student.py

from App.models import Student, Position, Application, Shortlist
from App.database import db


# 1. CREATE STUDENT + AUTO-GENERATE APPLICATIONS (GPA MATCHING)
def create_student(username, password, email, gpa, resume=None):

    new_student = Student(
        username=username,
        password=password,
        email=email,
        gpa=gpa,
        resume=resume
    )

    db.session.add(new_student)
    db.session.commit()

    # After creating the student check all positions for eligibility
    positions = Position.query.all()

    for pos in positions:
        if pos.gpa_requirement is None or gpa >= pos.gpa_requirement:
            # Automatically create Application record
            app = Application(student_id=new_student.id, position_id=pos.id)
            db.session.add(app)

    db.session.commit()

    return new_student.get_json(), 201



# 2. VIEW ALL APPLICATIONS (Track Stage)
def get_student_applications(student_id):

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return {"error": "Student not found"}, 404

    apps = Application.query.filter_by(student_id=student_id).all()

    return [{
        "application_id": a.id,
        "position_id": a.position_id,
        "status": a.status
    } for a in apps], 200



# 3. VIEW SHORTLISTED POSITIONS
def get_student_shortlisted_positions(student_id):

    entries = Shortlist.query.filter_by(student_id=student_id, isWithdrawn=False).all()

    return [{
        "shortlist_id": s.id,
        "position_id": s.position_id,
        "staff_id": s.staff_id,
        "status": s.status
    } for s in entries], 200



# 4. VIEW STATUS OF A SPECIFIC APPLICATION
def get_application_status(student_id, position_id):

    app = Application.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if not app:
        return {"error": "Application not found"}, 404

    return {"status": app.status}, 200



# 5. UPDATE STUDENT PROFILE 
def update_student_profile(student_id, gpa=None, resume=None):

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return {"error": "Student not found"}, 404

    # If GPA changes,need to regenerate eligibility
    gpa_changed = False

    if gpa is not None:
        student.gpa = gpa
        gpa_changed = True

    if resume is not None:
        student.resume = resume

    db.session.commit()

    # If GPA changed  recalc eligibility across positions
    if gpa_changed:
        refresh_student_applications(student_id)

    return {"message": "Profile updated"}, 200



# 6. GET ALL POSITIONS STUDENT IS ELIGIBLE FOR 
def get_eligible_positions_for_student(student_id):

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return {"error": "Student not found"}, 404

    positions = Position.query.all()
    eligible = []

    for p in positions:
        if p.gpa_requirement is None or student.gpa >= p.gpa_requirement:
            eligible.append(p.toJSON())

    return eligible, 200



#Refresh Application table after GPA change
def refresh_student_applications(student_id):

    student = Student.query.filter_by(id=student_id).first()
    positions = Position.query.all()

    # Remove old applications
    Application.query.filter_by(student_id=student_id).delete()

    # Recreate valid ones
    for pos in positions:
        if pos.gpa_requirement is None or student.gpa >= pos.gpa_requirement:
            app = Application(student_id=student_id, position_id=pos.id)
            db.session.add(app)

    db.session.commit()

