from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # Список всех активных подключений
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # Отправка сообщения всем сразу
        for connection in self.active_connections:
            await connection.send_text(message)

# Создаем один экземпляр на все приложение
manager = ConnectionManager()