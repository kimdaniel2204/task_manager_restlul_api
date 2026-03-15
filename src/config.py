import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Класс для хранения конфигурационных настроек приложения. Читает значения из переменных окружения.
class Settings:

    PROJECT_NAME: str = "Task Manager API"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL","sqlite:///./sql_app.db")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    ALGORITHM: str = "HS256"

    TELEGRAM_TOKEN: str | None = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID: str | None = os.getenv("TELEGRAM_CHAT_ID")


# Проверка, чтобы приложение не стартовало без SECRET_KEY
if not Settings.SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set. Please define it in environment variables."
    )


settings = Settings()