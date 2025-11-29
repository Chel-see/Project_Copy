from App.database import db
from App.models.user import User
from App.models.application import Application
from App.models.context import Context


class Shortlist(Application):  # because an application can exit and be a shortlisted application
    __tablename__ = 'shortlist'
    id = db.Column(db.Integer, db.ForeignKey('application.id'), primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    isWithdrawn = db.Column(db.Boolean, default=False)
    
    staff = db.relationship('Staff', backref=('shortlist'), lazy=True)


    def __init__(self, student_id, position_id, staff_id):  # an application will be created first with a position and by a student
       super().__init__(student_id,position_id)             # initialize the parent class so i can have access to student_id and position_id
       self.staff_id = staff_id
         

    
    def checkWithdrawn(self):
        return self.isWithdrawn

    @classmethod
    def student_shortlist(cls, student_id):  # gets all the short list for a particular student
        return cls.query.filter_by(student_id=student_id).all()

    @classmethod 
    def position_shortlist(cls, position_id): # gets all the short list for a particular position
        return cls.query.filter_by(position_id=position_id).all()
        
    def toJSON(self):
        return{
            "id": self.id,
            "student_id": self.student_id,
            "position_id": self.position_id,
            "staff_id": self.staff_id
        }
      
    __mapper_args__={'polymorphic_identity':'shortlist'}


