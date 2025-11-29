from App.models import Staff, Position, Student, Shortlist, Application
from App.database import db
from App.controllers.shortlist import get_eligible_students


# 1. CREATE STAFF ACCOUNT 
def create_staff(username, password, email, phone_number=None):  
    # Basic validation
    if not username or not password or not email:
        print("Staff creation failed: missing required fields")
        return None
        
    staff = Staff(username, password, email, phone_number)
    db.session.add(staff)
    db.session.commit()

    print(f"Staff '{username}' created successfully!")
    return staff


# 2. GET STAFF BY ID
def get_staff(staff_id):
    staff = Staff.query.filter_by(id=staff_id).first()
    if not staff:
        print("Staff not found")
        return None
    return staff


# 3. LIST ALL STAFF MEMBERS
def get_all_staff():
    return Staff.query.all()


# 4. VIEW ELIGIBLE STUDENTS FOR A POSITION
def staff_view_eligible_students(staff_id, position_id):

    staff = Staff.query.filter_by(id=staff_id).first()
    if not staff:
        return None

    return get_eligible_students(position_id) 


# 5. STAFF SHORTLISTS A STUDENT
def staff_shortlist_student(staff_id, student_id, position_id):

    staff = Staff.query.get(staff_id)
    student = Student.query.get(student_id)
    position = Position.query.get(position_id)

    if not staff:
        print("Staff not found")
        return None
    if not student:
        print("Student not found")
        return None
    if not position:
        print("Position not found")
        return None

    # Must have an application entry
    app = Application.query.filter_by(student_id=student_id, position_id=position_id).first()
    if not app:
        print("Student has no application for this position")
        return None

    # Must be eligible
    eligible_list, _ = get_eligible_students(position_id)
    eligible_ids = [e["student_id"] for e in eligible_list] 

    if student_id not in eligible_ids:
        print("Student does NOT meet GPA requirement")
        return None

    # Prevent duplicate shortlist
    existing = Shortlist.query.filter_by(student_id=student_id, position_id=position_id).first()
    if existing:
        print("Student is already shortlisted")
        return None

    # Create shortlist entry
    shortlist = Shortlist(
        student_id=student_id,
        position_id=position_id,
        staff_id=staff_id
    )
    db.session.add(shortlist)

    # Update parent Application state
    shortlist.setStatus("shortlisted")

    db.session.commit()

    print(f"Student {student_id} successfully shortlisted for Position {position_id}")
    return shortlist


# 6. STAFF SHORTLIST HISTORY
def staff_shortlist_history(staff_id):

    staff = Staff.query.get(staff_id)
    if not staff:
        return None

    return Shortlist.query.filter_by(staff_id=staff_id).all()
