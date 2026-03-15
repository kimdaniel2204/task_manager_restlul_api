from sqlalchemy.orm import Session
from typing import Optional

from src.models.user import User

# Репозиторий для работы с пользователями. Содержит методы для получения пользователя по email и создания нового пользователя в базе данных.
class UserRepository:

    def __init__(self, db: Session):
        self.db = db

# Метод для получения пользователя по email. 
    def get_by_email(self, email: str) -> Optional[User]:
        return (
            self.db
            .query(User)
            .filter(User.email == email)
            .first()
        )

# Метод для создания нового пользователя
    def create(self, email: str, hashed_password: str) -> User:

        db_user = User(
            email=email,
            hashed_password=hashed_password)
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user