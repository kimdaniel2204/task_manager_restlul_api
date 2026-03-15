from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.repositories.user_repository import UserRepository
from src.schemas.user import UserCreate
from src.services.security import hash_password, verify_password


# Сервис для работы с аутентификацией и регистрацией пользователей. Содержит методы для регистрации нового пользователя и аутентификации существующего пользователя.
class AuthService:

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

# Метод для регистрации нового пользователя
    def register_user(self, user: UserCreate):

        existing_user = self.user_repo.get_by_email(user.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        hashed_pwd = hash_password(user.password)

        return self.user_repo.create(
            email=user.email,
            hashed_password=hashed_pwd
        )

# Метод для аутентификации пользователя.
    def authenticate_user(self, email: str, password: str):

        user = self.user_repo.get_by_email(email)
        
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user