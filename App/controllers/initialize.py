from App.database import db

from .staff import create_staff,staff_shortlist_student
from .employer import create_employer
from .student import create_student
from .position import open_position

def initialize():
    db.drop_all()
    db.create_all()

    create_employer("jane", "janepass", "jane@gmail.com", "Jane's Company", "789-0123") # id=1
    create_staff("mary", "marrypass", "marryan@gmail.com","123-3456")   # id=2
    create_student("bob","bobpass","bob@gmail.com","222-3333","Computer Science",
                   "This internship will help me to grow my skills.","2000-05-15",3.5) # id=3

    open_position(1,"Web Developer", 2, gpa_requirement=2.5) # id=1
    staff_shortlist_student(2, 3,1)

   




