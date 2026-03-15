from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

# Модель пользователя. Содержит email, хеш пароля и связь с задачами, которыми владеет пользователь.
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    tasks = relationship(
        "Task", 
        back_populates="owner",
        cascade="all, delete"
    )