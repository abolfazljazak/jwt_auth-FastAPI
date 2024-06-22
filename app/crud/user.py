from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


class UserBusinessLogicLayer:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate, hashed_password: str):
        user = User(username=user.username, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class UserDataAccessLayer:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> User | None:
        user = self.db.query(User).filter_by(username=username).first()
        return user
