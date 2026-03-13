from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# строка подключения к БД
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@127.0.0.1:5444/task_db"

# движок БД
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# базовый класс для моделей
Base = declarative_base()


# dependency для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()