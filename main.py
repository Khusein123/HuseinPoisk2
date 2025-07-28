
import os
from dotenv import load_dotenv
load_dotenv()
import telebot
import threading
import time
from flask import Flask
from keep_alive import keep_alive
from monitor import MonitorManager
from userauth import UserAuth
from menu import MenuBuilder

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(TOKEN)

auth = UserAuth()
monitor = MonitorManager(bot, auth)
menu = MenuBuilder(bot)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    menu.send_main_menu(message.chat.id)

@bot.message_handler(func=lambda m: m.text == "🔍 Поиски")
def start_search(m):
    monitor.command_monitor(m)

@bot.message_handler(func=lambda m: m.text == "📄 Инструкция")
def show_help(m):
    bot.send_message(m.chat.id, '''Как Пользоваться ботом 👇

1. Для начала Вам необходимо приобрести уникальный ключ в разделе 'Аккаунт'.

2. После этого:
- Зайдите на сайт Avito.ru
- В поиске вбейте название вашего товара
- Настройте необходимые фильтры
- Скопируйте ссылку из адресной строки браузера

‼️ Обязательно укажите максимальную цену при настройке фильтров Авито. 
Если максимальная цена не имеет значения, укажите любую максимально большую цену, например, 100000000. 
Если этого не сделать, то будет бесконечная проверка ссылки.

⁉️ Если у Вас возникли проблемы с созданием ссылки или Вы хотите убедиться в её корректности, 
напишите в поддержку 👉 @Meneger_PoiskIphone.
''')

@bot.message_handler(func=lambda m: m.text == "💼 Поддержка")
def support(m):
    bot.send_message(m.chat.id, "Напишите @Meneger_PoiskIphone по вопросам активации ключей.")

@bot.message_handler(func=lambda m: m.text == "👤 Аккаунт")
def account(m):
    user_id = str(m.from_user.id)
    if auth.is_key_active(user_id):
        bot.send_message(m.chat.id, "✅ Ключ активен.")
    else:
        bot.send_message(m.chat.id, "❌ Ключ не активирован. Введите: /activate КЛЮЧ")

@bot.message_handler(commands=['activate'])
def activate_key(m):
    parts = m.text.split()
    if len(parts) == 2:
        result = auth.activate_key(str(m.from_user.id), parts[1])
        bot.send_message(m.chat.id, result)
    else:
        bot.send_message(m.chat.id, "❗ Формат: /activate КЛЮЧ")

@bot.message_handler(commands=['genkey'])
def generate_key(m):
    if str(m.chat.id) == CHAT_ID:
        key = auth.generate_key()
        bot.send_message(m.chat.id, f"🔑 Новый ключ: {key}")
    else:
        bot.send_message(m.chat.id, "⛔ Только администратор может генерировать ключи.")

keep_alive()
threading.Thread(target=monitor.loop).start()
bot.polling(none_stop=True)

