from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config import Settings
from src.services.websocket_manager import manager
from src.database import Base, engine
from src.models import user, task
from src.api import auth, task



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Ловит ошибки типа 404, 401, 403 и возвращает красивый JSON"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "code": exc.status_code
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    #Ловит вообще все ошибки, которые мы не обработали вручную (500-е)
    # Здесь можно добавить отправку ошибки в Телеграм, чтобы ты знал о багах сразу
    print(f"Глобальная ошибка: {str(exc)}") # Лог в консоль
    
    return JSONResponse(
        status_code=500,
        content={
            "status": "critical_error",
            "message": "Что-то пошло совсем не так на стороне сервера",
            # Если в .env DEBUG=True, покажет причину (удобно для разработки)
            # Если DEBUG=False, юзер увидит только общее сообщение (безопасно для продакшена)
            "details": str(exc) if Settings.DEBUG else "Internal Server Error"
        },
    )

app.include_router(auth.router)
app.include_router(task.router)

@app.get("/")
def root():
    return {"message": "API работает"}

@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)