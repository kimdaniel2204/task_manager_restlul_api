# slim — меньше размер, быстрее билд
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем файл зависимостей отдельно
# Это позволяет Docker кэшировать слой
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .

# Открываем порт, на котором работает FastAPI
EXPOSE 8000

# Команда запуска приложения
# uvicorn используется как ASGI-сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]