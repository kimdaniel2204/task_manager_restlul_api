from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config import Settings
from src.services.websocket_manager import manager
from src.database import Base, engine
from src.models import user, task
from src.api import auth, task



#Base.metadata.create_all(bind=engine)  закомментировал, т.к. миграции теперь через Alembic, 
                                        #и эта строка может вызвать проблемы с синхронизацией схемы БД.

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем доступ всем
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"],  # Разрешаем любые заголовки
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
# Обрабатывает стандартные HTTP ошибки (404, 401, 403 и т.д.)
#     и возвращает их в едином JSON формате
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
    #    Глобальный обработчик ошибок.
    # Срабатывает, если ошибка не была обработана явно.
    print(f"Глобальная ошибка: {str(exc)}")
    
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

# Роуты авторизации и управления задачами
app.include_router(auth.router)

# Роуты работы с задачами
app.include_router(task.router)


# Роуты для статических файлов и HTML страниц
app.mount("/static", StaticFiles(directory="static"), name="static")

# Эти роуты возвращают HTML страницы для дашборда, регистрации и логина.
@app.get("/dashboard")
async def get_dashboard():
    return FileResponse("static/dashboard.html")

@app.get("/register")
async def get_register_page():
    return FileResponse("static/register.html")

@app.get("/login")
async def get_login_page():
    return FileResponse("static/login.html")

@app.get("/")
def root():
    return {"message": "API работает"}


# Роут для WebSocket соединения. Клиенты будут подключаться сюда для получения real-time обновлений о задачах.
@app.websocket("/ws")  
async def websocket_endpoint(websocket: WebSocket):
    # await websocket.accept() # Закоммитил, не нужно,тк это уже внутри connect() вызывается
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)