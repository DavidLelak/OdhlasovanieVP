from sqlalchemy.orm import Session
from models import User
from werkzeug.security import generate_password_hash

# Vytvorenie používateľa
def create_user(db: Session, username: str, password: str, role: str = "user"):
    hashed_password = generate_password_hash(password)
    user = User(username=username, hashed_password=hashed_password, role=role, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Získanie všetkých používateľov
def get_all_users(db: Session):
    return db.query(User).all()

# Vymazanie používateľa
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

# Zmena aktívneho stavu používateľa
def set_user_active_status(db: Session, user_id: int, is_active: bool):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_active = is_active
        db.commit()
        db.refresh(user)
        return user
    return None

# Získanie používateľa podľa mena
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()