from App.database import db
from App.models.user import User
from sqlalchemy import Enum
import enum  
from App.models.context import Context


class Shortlist(db.Model):
    __tablename__ = 'shortlist'
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    status= db.Column(db.String(50))
    

    student= db.relationship('Student', backref=('shortlist'), lazy=True)
    position = db.relationship('Position', backref=('shortlist'), lazy=True)
    staff = db.relationship('Staff', backref=('shortlist'), lazy=True)


    def __init__(self, student_id, position_id, staff_id):
        self.student_id = student_id
        self.position_id = position_id
        self.staff_id = staff_id
        self.status ="shortlisted"
      
      
    def getStatus(self):
        return self.status
    
    def setStatus(self, context:Context): 
        self.status = context.getStateName()

    def student_shortlist(self, student_id):  # gets all the short list for a particular student
        return db.session.query(Shortlist).filter_by(student_id=student_id).all()

    def position_shortlist(self, position_id): # gets all the short list for a particular position
        return db.session.query(Shortlist).filter_by(position_id=position_id).all()
        
    def toJSON(self):
        return{
            "id": self.id,
            "student_id": self.student_id,
            "position_id": self.position_id,
            "staff_id": self.staff_id,
            "status": self.getStatus()
        }
      