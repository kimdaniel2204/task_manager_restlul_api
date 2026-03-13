import requests
from src.config import settings

class TelegramService:
    def __init__(self):
        self.token = settings.TELEGRAM_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_notification(self, text: str):
        if not self.token or not self.chat_id:
            print("Telegram credentials not found")
            return
            
        payload = {
            "chat_id": self.chat_id,
            "text": text
        }
        try:
            requests.post(self.api_url, json=payload, timeout=5)
        except Exception as e:
            print(f"Telegram error: {e}")