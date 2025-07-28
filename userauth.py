import time
import random
import string
import json
import os

class UserAuth:
    def __init__(self):
        self.file = "user_keys.json"
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def generate_key(self, duration_days=30):
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        expire = int(time.time()) + duration_days * 86400
        self.data[key] = {"user_id": None, "expire": expire}
        self.save()
        return key

    def activate_key(self, user_id, key):
        if key in self.data and self.data[key]["user_id"] is None:
            self.data[key]["user_id"] = user_id
            self.save()
            return "✅ Ключ успешно активирован!"
        elif key in self.data and self.data[key]["user_id"] == user_id:
            return "✅ Ключ уже активирован на ваш аккаунт."
        else:
            return "❌ Неверный ключ."

    def is_key_active(self, user_id):
        # Проверяем, есть ли для данного пользователя активный ключ и не истек ли он
        current_time = int(time.time())
        for key, info in self.data.items():
            if info.get("user_id") == user_id:
                expire = info.get("expire", 0)
                if expire >= current_time:
                    return True
        return False
