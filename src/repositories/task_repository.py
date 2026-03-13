from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.task import Task, TaskPriority, TaskStatus


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

        # Если в Swagger выбрали статус, добавляем фильтр в SQL
        if status:
            query = query.filter(Task.status == status)
            
        # Если выбрали приоритет, добавляем и его
        if priority:
            query = query.filter(Task.priority == priority)

        return query.all()
    def get_by_id(self, task_id: int) -> Optional[Task]:

        return (
            self.db.query(Task)
            .filter(Task.id == task_id)
            .first()
        )


    def create(self, task: Task) -> Task:

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task


    def delete(self, task: Task):

        self.db.delete(task)
        self.db.commit()

    def update(self, task: Task, update_data: dict) -> Task:
        for key, value in update_data.items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        
        return task