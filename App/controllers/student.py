# App/controllers/student.py

from App.models import Student, Position, Application, Shortlist
from App.database import db


# 1. CREATE STUDENT + AUTO-GENERATE APPLICATIONS (GPA MATCHING)
def create_student(username, password, email, phone_number, degree, resume, dob, gpa):
    
    # ----------- VALIDATION CHECKS -----------
    if not username or not password or not email:
        print("Error: Missing required fields.")
        return None

    try:
        gpa = float(gpa)
    except:
        print("Error: GPA must be numeric.")
        return None

    if gpa < 0 or gpa > 4.5:
        print("Error: GPA must be between 0.0 and 4.5.")
        return None

    new_student = Student(
        username=username,
        password=password,
        email=email,
        phone_number=phone_number,
        degree=degree,
        resume=resume,
        dob=dob,
        gpa=gpa
        
    )

    db.session.add(new_student)
    db.session.commit()

    print(f"Student {username} created!")

    # After creating the student check all positions for eligibility
    positions = Position.query.all()
    
    for pos in positions:
        if pos.gpa_requirement is None or gpa >= pos.gpa_requirement:

            # prevent duplicates
            exists = Application.query.filter_by(
                student_id=new_student.id,
                position_id=pos.id
            ).first()

            if not exists:
                app = Application(student_id=new_student.id, position_id=pos.id)
                db.session.add(app)

    db.session.commit()
    return new_student



# 2. VIEW ALL APPLICATIONS (Track Stage)
def get_student_applications(student_id):

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        print("Error: Student not found.")
        return None

    apps = Application.query.filter_by(student_id=student_id).all()
    return apps

# 3. VIEW SHORTLISTED POSITIONS
def get_student_shortlisted_positions(student_id):

    student = Student.query.get(student_id)
    if not student:
        print("Error: Student not found.")
        return None

    return Shortlist.query.filter_by(student_id=student_id, isWithdrawn=False).all()

# 4. VIEW STATUS OF A SPECIFIC APPLICATION
def get_application_status(student_id, position_id):

    app = Application.query.filter_by(student_id=student_id, position_id=position_id).first()

    if not app:
        print("Error: Application not found.")
        return None

    return app.status

# 5. UPDATE STUDENT PROFILE 
def update_student_profile(student_id, gpa=None, resume=None):

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        print("Error: Student not found.")
        return None

    # GPA update validation
    if gpa is not None:
        try:
            gpa = float(gpa)
        except:
            print("Error: GPA must be numeric.")
            return None

        if gpa < 0 or gpa > 4.5:
            print("Error: GPA must be between 0.0 and 4.5.")
            return None

        student.gpa = gpa
        gpa_changed = True

    # Resume update
    if resume is not None:
        student.resume = resume

    db.session.commit()

    if gpa_changed:
        refresh_student_applications(student_id)

    print("Profile updated successfully.")
    return student

# 6. GET ALL POSITIONS STUDENT IS ELIGIBLE FOR 
def get_eligible_positions_for_student(student_id):
    
    student = Student.query.get(student_id)
    if not student:
        print("Error: Student not found.")
        return None

    positions = Position.query.all()
    eligible = []

    for p in positions:
        if p.gpa_requirement is None or student.gpa >= p.gpa_requirement:
            eligible.append(p)

    return eligible

#Refresh Application table after GPA change
def refresh_student_applications(student_id):
    
    student = Student.query.get(student_id)
    if not student:
        print("Error: Student not found.")
        return None

    positions = Position.query.all()

    # Clear old applications
    Application.query.filter_by(student_id=student_id).delete()

    # Re-create eligible applications
    for pos in positions:
        if pos.gpa_requirement is None or student.gpa >= pos.gpa_requirement:
            app = Application(student_id=student_id, position_id=pos.id)
            db.session.add(app)

    db.session.commit()

    print("Student applications refreshed based on updated GPA.")

