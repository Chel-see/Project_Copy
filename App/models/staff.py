from App.database import db
from App.models.user import User

class Staff(User):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, username, password, email, phone_number=None):
        super().__init__(username, password, email, phone_number)
        self.type = 'staff'  # important for polymorphism

    def get_json(self):
        return super().get_json()
