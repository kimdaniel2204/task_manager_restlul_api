from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.services.auth_service import AuthService
from src.services.security import create_access_token
from src.schemas.token import Token
from src.schemas.user import UserCreate, UserOut


# Роуты для регистрации и логина пользователей
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Роут для регистрации нового пользователя. Принимает email и пароль, создает нового юзера в БД и возвращает его данные (без пароля).
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.register_user(user_data)
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists"
        )
    return user


# Роут для логина. Принимает email и пароль, проверяет их и возвращает JWT токен для авторизации в других роутов.
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    auth_service = AuthService(db)
    user = auth_service.authenticate_user(
        form_data.username,
        form_data.password
    )

# Если пользователь не найден или пароль неверный, возвращает 401 ошибку. 
# Иначе - создаем JWT токен и возвращаем его клиенту.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }