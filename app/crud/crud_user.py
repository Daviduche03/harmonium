
# app/crud/crud_user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
# from app.core.auth import get_password_hash

from passlib.context import CryptContext


from sqlalchemy.orm import Session
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user