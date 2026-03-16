import json

from src.utils.logger import logger
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # Список всех активных подключений
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        if websocket not in self.active_connections:
            self.active_connections.append(websocket)
            logger.info(f"Активных соединений: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        json_message = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(json_message)
            except Exception:
                continue

# Создаем один экземпляр на все приложение
manager = ConnectionManager()