from sqlalchemy.orm import Session
from typing import Optional

from src.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        return (
            self.db
            .query(User)
            .filter(User.email == email)
            .first()
        )

    def create(self, email: str, hashed_password: str) -> User:

        db_user = User(
            email=email,
            hashed_password=hashed_password
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user