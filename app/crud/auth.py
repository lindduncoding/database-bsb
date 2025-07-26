import os
import jwt
from datetime import datetime, timedelta, timezone
from models.users import User
from sqlalchemy.orm import Session
from utils.security import verify_password
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.user == username).first()
    if user and verify_password(password, user.password):
        return user
    return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt