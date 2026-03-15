import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from src.database import Base, get_db

# Используем SQLite в памяти для мгновенных тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Фикстура для настройки тестовой базы данных. 
# Создает все таблицы перед тестами и удаляет их после завершения тестов.
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Создает таблицы перед тестами и удаляет после"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Фикстура для получения сессии базы данных. 
# Открывает транзакцию перед тестом и откатывает ее после, чтобы обеспечить чистое состояние БД для каждого теста.
@pytest.fixture
def db_session():
    """Фикстура для работы с БД в тестах"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
    autouse=False

# Фикстура для клиента FastAPI, которая подменяет реальную базу данных на тестовую.
@pytest.fixture
def client(db_session):
    """Фикстура клиента, которая подменяет реальную БД на тестовую"""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()