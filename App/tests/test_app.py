import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Position, Shortlist, Staff, Student, PositionStatus, Application # remove context 
from App.models.applied_state import AppliedState
from App.models.shortlisted_state import ShortListedState
from App.models.accepted_state import AcceptedState
from App.models.rejected_state import RejectedState
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    open_position,
    get_positions_by_employer,
    # add_student_to_shortlist removed
    get_shortlist_by_student,
    decide_shortlist,
    staff_shortlist_student,
    create_student,
    create_staff,
    create_employer,
    get_position,
    get_position_by_title,
    get_student_shortlisted_positions
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_00_new_user(self):
        user = User("boblin", "boblinpass","boblin@gmail.com","111-2233")
        assert user.username == "boblin"

    def test_01_new_student(self):
            student = Student("john", "johnpass","john@example.com","555-1234","Computer Science","I am good  at computer science","2000-01-01",gpa=3.8)
            assert student.username == "john"
            assert student.type == "student"

    def test_02_new_staff(self):
        staff = Staff("jim", "jimpass", "jim@example.com","245-0098")
        assert staff.username == "jim"
        assert staff.type == "staff"
        assert staff.email == "jim@example.com"
        assert staff.phone_number == "245-0098"

    def test_03_new_employer(self):
        employer = Employer("alice", "alicepass","alice@example.com","Wonderland Inc.","333-5678")
        assert employer.username == "alice"
        assert employer.type == "employer"

    def test_04_new_position(self):
        position = Position("Software Developer",1,10, 3.0)  # employer id=1 from initialize 
        assert position.title == "Software Developer"
        assert position.employer_id == 1
        assert position.status == PositionStatus.open  # becuase it is an Enum not string 
        assert position.number_of_positions == 10
        assert position.gpa_requirement == 3.0


        
    def test_05_applied_state(self):
        state = AppliedState()
        # Check correct name
        assert state.getStateName() == "Applied"
        

    def test_06_rejected_state(self):
        state = RejectedState()
        name = state.getStateName()
        assert name=="Rejected"
    
    # pure function no side effects or integrations called
    def test_07_get_json(self):
        user = User("bobbyJoe", "bobpass","bob@gmail.com","123-4567")
        user_json = user.get_json()
        self.assertEqual(user_json["username"], "bobbyJoe")
        self.assertTrue("id" in user.get_json())
    
    def test_08_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password)
        user = User("boblinch", password,"boblinch@gmail.com","555-6789")
        assert user.password != password

    def test_09_check_password(self):
        password = "mypass"
        user = User("bobway", password,"bobway@gmail.com","987-6543")
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")  # change to module so all th etest will use the same DB 
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    
    with app.app_context():
        create_db()
        yield app.test_client()
        db.drop_all()

# @pytest.fixture(autouse=True, scope="module")
# def empty_db():
#     app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
#     create_db()
#     yield app.test_client()
#     db.drop_all()



class UserIntegrationTests(unittest.TestCase):
    # INCOOPERATE CREATING A SHORTLIST IF IT SNOT ALREADY HERE

    def test_10_create_user(self):
        # we use the controllers , their polymorphic types are assigned automatically
        staff = create_staff("rick", "rickpass","rickymartin@gmail.com","555-6789")
        assert staff is not None

        employer = create_employer("Sonny", "sampass","sam@example.com","AerilCo","555-1234")
        assert employer is not None

        student = create_student("hannah", "hannahpass","hannah@example.com","555-6789","Computer Engineering","Experienced in Computer engineering","1999-05-15",3.9 )
        assert student is not None
        
    def test_11_open_position(self):
        employer=get_user_by_username("Sonny")
        #assert employer is not None  # legit employer

        position=open_position(employer.id,"Backend Developer",5,2.5) 
        assert position.employer.id==employer.id  # validates that the foreign key relationship is correct
        assert position.title=="Backend Developer"
        assert position.number_of_positions==5
        assert position.gpa_requirement==2.5

        found_position=get_position(position_id=position.id ) # retrieves for DB
        assert found_position is not None
        

        


    def test_12_add_student_to_shortlist(self):  # all i need is staff , studnet and position
        student=create_student("Bake", "bakepass","bake@example.com","555-6789","Information Technology","Skille din web programming","2004-05-15",3.9)
        assert student is not None
        staff = get_user_by_username("rick")
        assert staff is not None
        position= get_position_by_title("Backend Developer")  # i have to have it seperatley bc a studnet can be shortlistsed for many positions and i need to compare a certain position to see if they are eligilbe
        assert position is not None
        shortlist=staff_shortlist_student(staff.id,student.id,position.id)

        assert shortlist.application.student_id == student.id
        assert shortlist.application.position_id == position.id
        assert shortlist.staff_id == staff.id
        assert shortlist.application.getStatus()=="Shortlisted"



        

    def test_13_decide_shortlist(self):
        # Create staff
        staff = create_staff("alice", "alicepass", "alice@example.com", "555-1111")
        assert staff is not None

        # Create employer
        employer = create_employer("bobco", "bobpass", "bobco@example.com", "BobCo Ltd", "555-2222")
        assert employer is not None

        # Create position for that employer
        position = open_position(employer.id, "Full Stack Dev", 2, 3.0)
        assert position is not None

        # Create student
        student = create_student("charlie", "charliepass", "charlie@example.com", "555-3333",
                                "Computer Science", "Experienced in Python", "2001-01-01", 3.5)
        assert student is not None

        # Ensure Application exists for student and position (create_student should do this)
        app = Application.query.filter_by(student_id=student.id, position_id=position.id).first()
        assert app is not None
        assert app.getStatus() == "Applied"

        # Staff shortlists the student
        shortlist = staff_shortlist_student(staff.id, student.id, position.id)
        assert shortlist is not None
        assert shortlist.application.getStatus() == "Shortlisted"

        # Employer decides to accept the student
        decided_shortlist = decide_shortlist(student.id, position.id, "accept")
        assert decided_shortlist is not None
        assert decided_shortlist.application.getStatus() == "Accepted"
       

        


    def test_14_student_view_shortlist(self):

        staff = create_staff("allan", "alllanass", "all@example.com", "555-1111")
        assert staff is not None

        employer =  create_employer("joella", "joeypass", "abctech@gmail.com","ABCTech","568-9907")
        assert employer is not None

        position = open_position(employer.id,"Software Eng", 4,2.0)
        assert position is not None

        student = create_student("Mason", "masonpass", "m@example.com", "555-333","Computer Science", "Experienced in Python", "2001-01-01", 3.5)
        assert student is not None


        shortlistSt= staff_shortlist_student(staff.id,student.id, position.id)
        assert shortlistSt is not None
        
        shortlists = get_shortlist_by_student(student.id)
        assert len(shortlists) > 0


    def test_15_application_state_transitions(self):
        
        staff = create_staff("Mailen", "mailpass","mail@gmail.com","555-6789")
        assert staff is not None

        employer = create_employer("Marsakin", "Marspass","Mars@example.com","DaCo","555-1234")
        assert employer is not None

        position = open_position(employer.id,"Jr Web Developer", 4,1.5)
        assert position is not None

        student = create_student("hannahta", "hannahtapass","hannahta@example.com","555-6789","Computer Engineering","Good at Java","1999-05-15",1.5 )
        assert student is not None


    #-----------Check Applied State---------------------------
        app=Application.query.filter_by(student_id=student.id,position_id=position.id).first()
        assert app.getStatus()=="Applied"

    #-----------Check Shortlisted State---------------------------
        shortlist=staff_shortlist_student(staff.id, student.id, position.id)
        assert shortlist.application.getStatus()=="Shortlisted"

    #-----------Transition to Rejected State through decision---------------------
        decision=decide_shortlist(student.id,position.id,"reject")
        assert decision.application.getStatus()=="Rejected"

    #-------------Check Previous------------------
        decision.application.previous()
        assert decision.application.getStatus()=="Shortlisted"
    
    #--------------Transition to Accepted State through decision-----------------------------------------
        decision=decide_shortlist(student.id,position.id,"accept")
        assert decision.application.getStatus()=="Accepted"

    #-----------Check Withdraw from Accepted----------------------------
        decision.application.withdraw()
        assert decision.application.getStatus()=="Rejected"



     

    # Tests data changes in the database
    #def test_update_user(self):
    #    update_user(1, "ronnie")
    #   user = get_user(1)
    #   assert user.username == "ronnie"

