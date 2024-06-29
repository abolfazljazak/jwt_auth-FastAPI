from datetime import (
    datetime,
    timedelta
)
from sqlalchemy.orm import Session
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.models.user import User

from app.crud.user import UserDataAccessLayer


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    def __init__(self, DAL: UserDataAccessLayer):
        self.dal = DAL

    def get_password_hash(self, password):
        password_hash = pwd_context.hash(password)
        return password_hash

    def verify_password(self, plain_password, hashed_password):
        verify_password = pwd_context.verify(plain_password, hashed_password)
        return verify_password

    def authenticate_user(self, username: str, hashed_password: str):
        user = self.dal.get_user_by_username(username)
        if not user or not self.verify_password(user.password, hashed_password):
            return None

        return user



class JWTService:

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta

        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

