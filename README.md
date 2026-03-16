# Task Manager RESTful API

Backend API для управления задачами с аутентификацией, realtime-уведомлениями и простым frontend.

Проект создан как pet-project для демонстрации backend-навыков.



## Возможности

- Регистрация и авторизация пользователей (JWT)
- CRUD операции для задач
- Защищённые эндпоинты
- WebSocket уведомления в реальном времени
- Telegram уведомления
- Frontend страницы (login / register / dashboard)
- Swagger документация

---

## Технологии

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT (python-jose)
- WebSockets
- Passlib (bcrypt)
- Pytest
- Bootstrap (frontend)

---

## Структура проекта
task_manager/
│
├── main.py
├── src/
│ ├── api/ # Роуты (auth, tasks)
│ ├── models/ # SQLAlchemy модели
│ ├── services/ # Логика (security, websocket, telegram)
│ ├── database.py # Подключение к БД
│ └── config.py # Настройки приложения
│ └── schemas
│
├── static/ # HTML страницы
├── tests/ # Тесты backend
├── .env.example
└── README.md
└── docker-compose


---

## Установка и запуск через Docker (рекомендуется)

1. Склонируйте репозиторий.
2. Создайте файл .env в корне проекта и укажите необходимые переменные (токен Telegram, секретный ключ).
3. Запустите проект одной командой:
   ```bash
   docker-compose up -d --build





# 1 Установка и запуск в ручную

1 Клонируйте репозиторий

```bash
git clone https://github.com/kimdaniel2204/task-manager-restful-api.git
cd task-manager-restful-api

# 2 Создать виртуальное окружение

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

# 3 Установить зависимости

pip install -r requirements.txt

# 4 создать .env файл

cp .env.example .env

# 5 запустить сервер

uvicorn main:app --reload


# Документация API
# Swagger доступен по адресу:

http://127.0.0.1:8000/docs


# Аутентификация
# Используется JWT Bearer Token.

# 1 Зарегистрироваться: POST /auth/register
# 2 Войти: POST /auth/login
# 3 Использовать токен в заголовке:


# WebSocket
# Endpoint для realtime-уведомлений:

ws://127.0.0.1:8000/ws

# Тестовая страница:

/static/test_ws.html


# 6 Тесты

Backend полностью покрыт тестами.
Тесты написаны до разработки frontend-части.

Запуск тестов:

python -m pytest
