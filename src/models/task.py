from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from src.database import Base


# Модель задачи. Содержит поля для названия, описания, дедлайна, статуса, приоритета, времени создания и связи с пользователем-владельцем.
class TaskStatus(enum.Enum):
    new = "new"
    in_progress = "in_progress"
    completed = "completed"

# Приоритет задачи. Может быть low, medium или high. По умолчанию - medium.
class TaskPriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

# Основная модель задачи. Содержит все поля, необходимые для хранения инфо о задаче в базе данных
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    priority = Column(SqlEnum(TaskPriority), default=TaskPriority.medium)
    status = Column(SqlEnum(TaskStatus), default=TaskStatus.new)
    description = Column(String, nullable=True)

    # Дедлайн задачи. Может быть null, если дедлайн не установлен.
    deadline = Column(DateTime, nullable=True)

    # Поле для хранения информации о том, просрочена ли задача
    is_overdue = Column(Boolean, default=False)
    
    # Время создания задачи
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с пользователем-владельцем задачи. один ко многим
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")