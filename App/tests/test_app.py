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
    get_position_by_title
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
        position_count = 3
        student = create_user("jack", "jackpass", "student")
        assert student is not None
        staff = create_user ("pat", "patpass", "staff")
        assert staff is not None
        employer =  create_user("frank", "pass", "employer")
        assert employer is not None
        position = open_position("Intern", employer.id, position_count)
        assert position is not None
        stud_shortlist = add_student_to_shortlist(student.id, position.id ,staff.id)
        assert (stud_shortlist)
        decided_shortlist = decide_shortlist(student.id, position.id, "accepted")
        assert (decided_shortlist)
        shortlists = get_shortlist_by_student(student.id)
        assert any(s.status == PositionStatus.accepted for s in shortlists)
        assert position.number_of_positions == (position_count-1)
        assert len(shortlists) > 0
        invalid_decision = decide_shortlist(-1, -1, "accepted")
        assert invalid_decision is False


    def test_14_student_view_shortlist(self):

        student = create_user("john", "johnpass", "student")
        assert student is not None
        staff = create_user ("tim", "timpass", "staff")
        assert staff is not None
        employer =  create_user("joe", "joepass", "employer")
        assert employer is not None
        position = open_position("Software Intern", employer.id, 4)
        assert position is not None
        shortlist = add_student_to_shortlist(student.id, position.id ,staff.id)
        shortlists = get_shortlist_by_student(student.id)
        assert any(shortlist.id == s.id for s in shortlists)
        assert len(shortlists) > 0

    def test_15_application_state_transitions(self):
        # Initial state: Applied
        app = Application(1, 1)
        assert isinstance(app.context.state, AppliedState)
        assert app.getStatus() == "applied"

        # ---------- Next transitions ----------
        app.setStatus("shortlisted")  # Applied → Shortlisted
        assert isinstance(app.context.state, ShortListedState)
        assert app.getStatus() == "shortlisted"

        app.setStatus("accept")  # Shortlisted → Accepted
        assert isinstance(app.context.state, AcceptedState)
        assert app.getStatus() == "accepted"

        app.setStatus("shortlisted")  # Back to Shortlisted to test rejection
        app.setStatus("reject")  # Shortlisted → Rejected
        assert isinstance(app.context.state, RejectedState)
        assert app.getStatus() == "rejected"

        # ---------- Previous transitions ----------
        app.context.previous()  # Rejected → Shortlisted
        assert isinstance(app.context.state, ShortListedState)
        assert app.getStatus() == "shortlisted"

        app.context.previous()  # Shortlisted → Applied
        assert isinstance(app.context.state, AppliedState)
        assert app.getStatus() == "applied"

        app.setStatus("shortlisted")
        app.setStatus("accept")
        app.context.previous()  # Accepted → Shortlisted
        assert isinstance(app.context.state, ShortListedState)
        assert app.getStatus() == "shortlisted"

        # ---------- Withdraw transitions ----------
        app.setStatus("shortlisted")
        app.context.withdraw()  # Shortlisted → Rejected
        assert isinstance(app.context.state, RejectedState)
        assert app.getStatus() == "rejected"

        app.setStatus("accept")
        app.context.withdraw()  # Accepted → Rejected
        assert isinstance(app.context.state, RejectedState)
        assert app.getStatus() == "rejected"

        app.setStatus("applied")
        app.context.withdraw()  # Applied → Applied (no-op)
        assert isinstance(app.context.state, AppliedState)
        assert app.getStatus() == "applied"

        app.setStatus("reject")
        app.context.withdraw()  # Rejected → Rejected (no-op)
        assert isinstance(app.context.state, RejectedState)
        assert app.getStatus() == "rejected"

        # ---------- No-op transitions ----------
        app.setStatus("applied")
        app.context.previous()  # No previous from Applied
        assert isinstance(app.context.state, AppliedState)
        assert app.getStatus() == "applied"

        app.setStatus("accept")
        app.context.next()  # No next from Accepted
        assert isinstance(app.context.state, AcceptedState)
        assert app.getStatus() == "accepted"

        app.setStatus("reject")
        app.context.next()  # No next from Rejected
        assert isinstance(app.context.state, RejectedState)
        assert app.getStatus() == "rejected"

    # Tests data changes in the database
    #def test_update_user(self):
    #    update_user(1, "ronnie")
    #   user = get_user(1)
    #   assert user.username == "ronnie"

