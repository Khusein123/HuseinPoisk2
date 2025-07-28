from telebot import types

class MenuBuilder:
    def __init__(self, bot):
        self.bot = bot

    def send_main_menu(self, chat_id):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("🔍 Поиски", "📄 Инструкция")
        kb.row("💼 Поддержка", "👤 Аккаунт")
        self.bot.send_message(chat_id, "Выберите действие:", reply_markup=kb)