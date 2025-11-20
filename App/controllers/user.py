from App.models import User, Student, Employer, Staff
from App.database import db

def create_user(username, password, email, phone_number, user_type):
    try:
        type_map = {
            "student": Student,
            "employer": Employer,
            "staff": Staff
        }

        UserClass = type_map.get(user_type)
        if not UserClass:
            return False
        
        new_user = UserClass(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number
        )

        db.session.add(new_user)
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        return False


def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None
