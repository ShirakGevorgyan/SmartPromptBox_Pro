# app/telegram_bot/handlers/texts_handler.py

from aiogram import Dispatcher
from aiogram.types import Message

# 📚 Պահպանում ենք ամեն user-ի համար՝ {user_id: [{"url": ..., "lyrics": ...}]}
user_lyrics = {}

def save_lyrics(user_id: int, url: str, lyrics: str):
    if user_id not in user_lyrics:
        user_lyrics[user_id] = []
    user_lyrics[user_id].append({"url": url, "lyrics": lyrics})

def register(dp: Dispatcher):
    @dp.message_handler(lambda msg: msg.text == "📝 Անցած տեքստեր")
    async def show_past_lyrics(message: Message):
        user_id = message.from_user.id
        entries = user_lyrics.get(user_id, [])

        if not entries:
            await message.answer("📭 Դեռ չկան պահված երգերի տեքստեր։")
        else:
            for entry in entries:
                await message.answer(f"🎵 {entry['url']}\n\n📝 {entry['lyrics']}")
