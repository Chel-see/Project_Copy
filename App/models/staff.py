from App.database import db
from App.models.user import User
from App.models.shortlist import Shortlist

class Staff(User):
    __tablename__ = 'staff'

    # Staff uses the User.id as its primary key
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, username, password, email, phone_number=None):
        super().__init__(username, password, email, phone_number)
        self.type = 'staff'

    def get_json(self):
        base = super().get_json()
        return base  # nothing extra to add

    # Staff business logic
    def add_to_shortlist(self, student_id, position_id):
        shortlist = Shortlist(
            student_id=student_id,
            position_id=position_id,
            staff_id=self.id
        )
        db.session.add(shortlist)
        db.session.commit()
        return shortlist
