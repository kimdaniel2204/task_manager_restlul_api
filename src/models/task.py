from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from src.database import Base


class TaskStatus(enum.Enum):
    new = "new"
    in_progress = "in_progress"
    completed = "completed"


class TaskPriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(String, nullable=True)

    deadline = Column(DateTime, nullable=True)

    status = Column(SqlEnum(TaskStatus), default=TaskStatus.new)

    priority = Column(SqlEnum(TaskPriority), default=TaskPriority.medium)

    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="tasks")