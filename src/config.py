import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    PROJECT_NAME: str = "Task Manager API"
        
        # Режим отладки: если True, сервер будет показывать детали ошибок.
        # В .env можно написать DEBUG=True
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
        
        # Настройки БД
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
        
        # Секреты для JWT (у тебя они наверняка уже есть)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

settings = Settings()