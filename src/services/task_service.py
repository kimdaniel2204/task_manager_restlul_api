from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from src.models.task import Task, TaskPriority, TaskStatus
from src.repositories.task_repository import TaskRepository
from src.schemas.task import TaskCreate, TaskUpdate

import io
import csv


# Сервис для работы с задачами
class TaskService:
    def __init__(self, db: Session): 
        self.task_repo = TaskRepository(db)

# Метод для получения списка задач текущего пользователя 
    def get_tasks(self, user_id: int, status: Optional[TaskStatus] = None, priority: Optional[TaskPriority] = None):
        return self.task_repo.get_user_tasks(user_id, status, priority)

# Метод для создания новой задачи
    def create_task(self, task_data: TaskCreate, user_id: int):
        task = Task(
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            priority=task_data.priority,
            owner_id=user_id
        )
        return self.task_repo.create(task)

# Метод для удаления задачи. Проверяет, что задача существует и принадлежит текущему пользователю, затем удаляет ее из базы данных.
    def delete_task(self, task_id: int, user_id: int):
        task = self.task_repo.get_by_id(task_id)
        if not task or task.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        self.task_repo.delete(task)
        return {"message": "Task deleted"}
    
    # Метод для обновления задачи. Проверяет, что задача существует и принадлежит текущему пользователю, затем обновляет ее поля на основе переданных данных и сохраняет изменения в базе данных.
    def update_task(self, task_id: int, user_id: int, update_data: TaskUpdate):
        task = self.task_repo.get_by_id(task_id)
        if not task or task.owner_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Превращаем схему в словарь, исключая неустановленные поля
        data = update_data.model_dump(exclude_unset=True) 
        return self.task_repo.update(task, data)
    
    def export_tasks_to_csv(self, user_id: int):
        tasks = self.task_repo.get_user_tasks(user_id)
        
        # Создаем буфер в памяти для записи текста
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Заголовки таблицы
        writer.writerow(['ID', 'Title', 'Description', 'Status', 'Priority', 'Deadline'])
        
        # Данные
        for task in tasks:
            writer.writerow([
                task.id, 
                task.title, 
                task.description, 
                task.status.value if task.status else "", 
                task.priority.value if task.priority else "", 
                task.deadline
            ])
            
        return output.getvalue()