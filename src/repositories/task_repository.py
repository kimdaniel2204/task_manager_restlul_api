from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.task import Task, TaskPriority, TaskStatus


# Репозиторий для работы с задачами. Содержит методы для получения, создания, обновления и удаления задач в базе данных.
class TaskRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_user_tasks(
        self, 
        user_id: int, 
        status: Optional[TaskStatus] = None, 
        priority: Optional[TaskPriority] = None
    ):
        # Создаем базовый запрос: "Дай все задачи этого юзера"
        query = self.db.query(Task).filter(Task.owner_id == user_id)

  
        if status:
            query = query.filter(Task.status == status)

        if priority:
            query = query.filter(Task.priority == priority)

        return query.all()
    
# Метод для получения задачи по ID. Возвращает задачу, если она существует, или None, если задачи с таким ID нет.
    def get_by_id(self, task_id: int) -> Optional[Task]:

        return (
            self.db.query(Task)
            .filter(Task.id == task_id)
            .first()
        )

# Метод для создания новой задачи. Принимает объект Task, сохраняет его в базе данных и возвращает сохраненный объект с заполненным ID.
    def create(self, task: Task) -> Task:

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

# Метод для удаления задачи. Принимает объект Task, удаляет его из базы данных и коммитит изменения.
    def delete(self, task: Task):

        self.db.delete(task)
        self.db.commit()

# Метод для обновления задачи. Принимает объект Task и словарь с данными для обновления, изменяет поля задачи, сохраняет изменения в базе данных и возвращает обновленный объект.
    def update(self, task: Task, update_data: dict) -> Task:
        for key, value in update_data.items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        
        return task