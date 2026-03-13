from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.task import TaskPriority, TaskStatus
from src.database import get_db
from src.schemas.task import TaskCreate, TaskOut, TaskUpdate
from src.services.task_service import TaskService
from src.services.security import get_current_user
from src.services.websocket_manager import manager
from src.services.telegram_service import TelegramService 

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# Выносим создание экземпляра сюда, чтобы не плодить импорты внутри функций
tg_service = TelegramService()

@router.get("/", response_model=List[TaskOut])

def get_tasks(
    status: Optional[TaskStatus] = None, 
    priority: Optional[TaskPriority] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_service = TaskService(db)
    return task_service.get_tasks(current_user.id, status, priority)

@router.get("/export/csv")

def export_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_service = TaskService(db)
    csv_data = task_service.export_tasks_to_csv(current_user.id)
    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=my_tasks.csv"}
    )

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)

async def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_service = TaskService(db)
    new_task = task_service.create_task(task, current_user.id)
    
    msg = f"New Task Created:\nTitle: {new_task.title}\nPriority: {new_task.priority.value}"
    background_tasks.add_task(tg_service.send_notification, msg)
    await manager.broadcast(f"Новая задача создана: {new_task.title}")
    
    return new_task

@router.patch("/{task_id}", response_model=TaskOut)

async def update_task(
    task_id: int,
    update_data: TaskUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_service = TaskService(db)
    updated_task = task_service.update_task(task_id, current_user.id, update_data)
    
    msg = f"Задача обновлена (ID: {task_id}):\nНовый статус: {updated_task.status.value}"
    background_tasks.add_task(tg_service.send_notification, msg)
    await manager.broadcast(f"Задача обновлена: {updated_task.title}")

    return updated_task # Возвращаем уже обновленный объект

@router.delete("/{task_id}")

async def delete_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_service = TaskService(db)
    # Выполняем удаление один раз
    result = task_service.delete_task(task_id, current_user.id)
    
    msg = f"Задача удалена:\nID: {task_id}"
    background_tasks.add_task(tg_service.send_notification, msg)
    await manager.broadcast(f"Задача удалена: {task_id}")

    return result # Здесь вернется {"message": "Task deleted"}