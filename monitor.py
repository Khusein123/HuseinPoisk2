import time
import requests
from bs4 import BeautifulSoup

class MonitorManager:
    def __init__(self, bot, auth):
        self.bot = bot
        self.auth = auth
        self.monitors = {}

    def command_monitor(self, message):
        user_id = str(message.from_user.id)
        if not self.auth.is_key_active(user_id):
            self.bot.send_message(message.chat.id, """❌ Для того чтобы начать поиск вам нужно приобрести Уникальный Ключ,
для того чтобы приобрести ключ напишите Менеджеру 👉@Meneger_PoiskIphone""")
            return
        msg = self.bot.send_message(message.chat.id, """Для того чтобы начать Поиск вам нужно:
Скопируйте ссылку Авито с вашим поиском.
Для этого в браузере на телефоне или на компьютере откройте Авито, настройте необходимые фильтры и скопируйте ссылку из адресной строки браузера.

‼️ Обязательно укажите максимальную цену при настройке фильтров Авито. Если максимальная цена не имеет значения, укажите любую большую цену, например 100000000. Если этого не сделать, то будет бесконечная проверка ссылки.

⁉️ Если у Вас возникли проблемы с созданием ссылки или Вы хотите убедиться в её корректности, напишите в поддержку 👉 @Meneger_PoiskIphone""")
        self.bot.register_next_step_handler(msg, self._process_link)

    def loop(self):
        while True:
            for user_id in list(self.monitors):
                chat_id = self.monitors[user_id]["chat"]
                data = self._fetch_items(self.monitors[user_id]["url"])
                current_links = [item["link"] for item in data]
                new_items = [item for item in data if item["link"] not in self.monitors[user_id].get("last_ids", set())]
                for item in new_items:
                    title = item.get("title") or "Новое объявление"
                    price = item.get("price")
                    link = item.get("link")
                    text = f"🔔 Новое объявление: {title}"
                    if price:
                        text += f" за {price}"
                    if link:
                        text += f"\n{link}"
                    self.bot.send_message(chat_id, text)
                if "last_ids" not in self.monitors[user_id]:
                    self.monitors[user_id]["last_ids"] = set()
                self.monitors[user_id]["last_ids"].update(current_links)
            time.sleep(300)

    def _process_link(self, message):
        user_id = str(message.from_user.id)
        url = message.text.strip()
        if not url:
            self.bot.send_message(message.chat.id, "❌ Ссылка не распознана.")
            return
        if not url.startswith("http"):
            url = "https://" + url
        self.monitors[user_id] = {"chat": message.chat.id, "url": url, "last_ids": set()}
        try:
            items = self._fetch_items(url)
            initial_links = [item["link"] for item in items]
            self.monitors[user_id]["last_ids"] = set(initial_links)
            self.bot.send_message(message.chat.id, "✅ Мониторинг объявлений запущен.")
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ Ошибка при получении данных: {e}")

    def _fetch_items(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")
        soup = BeautifulSoup(resp.text, 'html.parser')
        items_data = []
        for item in soup.find_all(attrs={"data-marker": "item"}):
            title = ""
            price = ""
            link = ""
            a_tag = item.find('a')
            if a_tag:
                title = a_tag.get_text(strip=True)
                href = a_tag.get('href')
                if href:
                    link = "https://www.avito.ru" + href if href.startswith('/') else href
            price_tag = item.find(attrs={"data-marker": "item-price"})
            if price_tag:
                price = price_tag.get_text(strip=True)
            else:
                price_text = item.find(text=lambda t: t and '₽' in t)
                if price_text:
                    price = price_text.strip()
            items_data.append({"title": title, "price": price, "link": link})
        return items_data
