import time
import requests

class MonitorManager:
    def __init__(self, bot, auth):
        self.bot = bot
        self.auth = auth
        self.monitors = {}

    def command_monitor(self, message):
        user_id = str(message.from_user.id)
        if not self.auth.is_key_active(user_id):
            self.bot.send_message(message.chat.id, "❌ У вас нет активного ключа.")
            return
        self.bot.send_message(message.chat.id, "Вставьте ссылку для мониторинга.")
        self.monitors[user_id] = {"active": True, "chat": message.chat.id}

    def loop(self):
        while True:
            for user_id in list(self.monitors):
                # Эмуляция (в реальности — сделать запрос и парсинг)
                chat_id = self.monitors[user_id]["chat"]
                self.bot.send_message(chat_id, "🔔 Новое объявление!")
            time.sleep(300)