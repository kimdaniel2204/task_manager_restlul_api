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


# Роуты для работы с задачами
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

tg_service = TelegramService()


# Роут для получения списка задач. 
# Поддерживает фильтрацию по статусу и приоритету. Возвращает только задачи текущего пользователя.
@router.get("/", response_model=List[TaskOut])

def get_tasks(
    status: Optional[TaskStatus] = None, 
    priority: Optional[TaskPriority] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_service = TaskService(db)
    return task_service.get_tasks(current_user.id, status, priority)

# Роут для экспорта задач в CSV. Возвращает файл с задачами текущего пользователя в виде CSV.
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

# Роут для создания новой задачи. Принимает данные задачи, создает ее в БД и возвращает созданную задачу.
@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)

async def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_service = TaskService(db)
    new_task = task_service.create_task(task, current_user.id)
    
    msg = f"Новая задача создана:\nНазвание: {new_task.title}\nПриоритет: {new_task.priority.value}"
    background_tasks.add_task(tg_service.send_notification, msg)
    await manager.broadcast(f"Новая задача создана: {new_task.title}")
    
    return new_task

# Роут для обновления задачи. Принимает ID задачи и данные для обновления, изменяет задачу в БД и возвращает обновленную задачу.
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
    
    msg = f"Задача обновлена (ID: {task_id}):\nНовый статус: {updated_task.status.value}:\nНовое название: {updated_task.title}"
    background_tasks.add_task(tg_service.send_notification, msg)
    await manager.broadcast(f"Задача обновлена: {updated_task.title}")

    return updated_task # Возвращаем уже обновленный объект

# Роут для удаления задачи. Принимает ID задачи, удаляет ее из БД и возвращает сообщение об успешном удалении.
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
    
    msg = f"Задача удалена:\nID: {task_id}:\nНазвание: {result.get('message', 'Unknown')}"
    background_tasks.add_task(tg_service.send_notification, msg)
    await manager.broadcast(f"Задача удалена: {task_id}")

    return result