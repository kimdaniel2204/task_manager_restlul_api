from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from src.models.task import TaskStatus, TaskPriority


# Схемы для работы с задачами 
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.medium

# Схема для создания новой задачи. Наследует все поля от TaskBase и не требует указания статуса, так как при создании задачи статус всегда будет "new".
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[TaskPriority] = TaskPriority.medium
    deadline: Optional[datetime] = None 

# Схема для обновления задачи. Все поля являются необязательными, так как при обновлении можно изменить только некоторые поля задачи
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

# Схема для вывода информации о задаче. 
class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    deadline: Optional[datetime]= None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    owner_id: int

# Настройка Pydantic для работы с моделями SQLAlchemy
class Config:
        from_attributes = True