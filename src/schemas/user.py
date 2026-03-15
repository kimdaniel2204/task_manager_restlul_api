from pydantic import BaseModel, EmailStr

# Поля для создания нового пользователя и вывода информации о пользователе.
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Схема для вывода информации о пользователе. Содержит id и email пользователя
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True