from config.database import SessionLocal
from config.database import engine
from config.database import Base
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from models.models import User
from Routes.bot import router as bot_router
from Routes.embedding_route import router as embedding_router
from typing import Annotated
from auth.auth_bearer import JWTBearer
from pydantic import BaseModel
from config.db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# JWT setup
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(debug=True)


# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to get user by username
def get_user(db, username: str):
    return db.query(User).filter(User.username == username).first()


# Function to authenticate user
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoints
@app.post("/signup/")
def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # Check if user already exists
    if get_user(db, username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if get_user(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = pwd_context.hash(password)

    # Create new user
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()

    return {"message": "User created successfully"}

@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return db.query(User).filter(User.id == username).first()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
class UserSchema(BaseModel):
    username: str
    email: str

@app.get("/users/me/")
async def read_users_me(current_user: UserSchema = Depends(get_current_user)):
    return current_user

app.include_router(bot_router)
app.include_router(embedding_router)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)