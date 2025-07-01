# app/telegram_bot/handlers/songs_handler.py

from aiogram import Dispatcher
from aiogram.types import Message

# 🔘 Dictionary՝ պահպանելու համար յուրաքանչյուր օգտատիրոջ հղումները
user_links = {}

def register(dp: Dispatcher):
    # 🎵 Մենյուից սեղմելու դեպքում
    @dp.message_handler(lambda msg: msg.text == "🎵 Ուղարկված երգեր")
    async def show_sent_songs(message: Message):
        user_id = message.from_user.id
        links = user_links.get(user_id, [])

        if not links:
            await message.answer("📭 Դու դեռ ոչ մի երգի հղում չես ուղարկել։")
        else:
            await message.answer("📄 Ահա քո ուղարկած YouTube հղումները՝\n\n" + "\n".join(links))

    # ✅ Արտաքին ֆունկցիա՝ ավելացնելու հղումները (կօգտագործվի lyrics_handler-ից)
    def save_link(user_id: int, link: str):
        if user_id not in user_links:
            user_links[user_id] = []
        if link not in user_links[user_id]:
            user_links[user_id].append(link)

    # 📌 Հնարավորություն՝ այլ ֆայլից էլ import անել save_link()
    global _save_link
    _save_link = save_link

# 🪄 Արտահանվող ֆունկցիա
def save_user_link(user_id: int, link: str):
    _save_link(user_id, link)
