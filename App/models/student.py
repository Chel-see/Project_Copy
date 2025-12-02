from App.database import db
from App.models.user import User

from datetime import date



class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer,db.ForeignKey('user.id'), primary_key=True)
    degree = db.Column(db.String(256))
    resume = db.Column(db.String(256))
    dob = db.Column(db.String(10))
    gpa = db.Column(db.Float)

    #applications = db.relationship("Application", backref="student", lazy=True)  # help to get the position

    __mapper_args__={"polymorphic_identity" : "student"}

    def __init__(self, username, password, email , phone_number, degree,resume, dob,gpa):
        super().__init__(username, password, email, phone_number)
        self.degree = degree
        self.resume = resume
        self.dob = dob
        self.gpa = gpa
      
    @staticmethod
    def get_student_by_username(username):
        return Student.query.filter_by(username=username).first()
   

    def __repr__(self):
        return f'<Student ID: {self.id} - Username: {self.username} - Degree: {self.degree}>'