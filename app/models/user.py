from sqlalchemy import Column, Integer, String
from app.database.base import Base


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    hashed_password: str = Column(String)
