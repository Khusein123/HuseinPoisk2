import json
import uuid
from datetime import datetime, timedelta

KEY_FILE = "keys.json"

try:
    with open(KEY_FILE, "r", encoding="utf-8") as f:
        keys = json.load(f)
except:
    keys = {}

def generate_key(days):
    key = uuid.uuid4().hex[:16].upper()
    expires = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    keys[key] = {"expires": expires}
    return key, expires

if __name__ == "__main__":
    print("Введите срок действия ключа (в днях): ", end="")
    try:
        days = int(input().strip())
    except:
        days = 30
    new_key, exp = generate_key(days)
    # Сохраняем новый ключ в файл
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        json.dump(keys, f, ensure_ascii=False, indent=2)
    print(f"Сгенерирован ключ: {new_key}, действует до {exp}")
