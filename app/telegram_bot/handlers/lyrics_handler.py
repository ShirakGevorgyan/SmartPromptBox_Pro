# app/telegram_bot/handlers/lyrics_handler.py

import re
import requests
from aiogram import Dispatcher
from aiogram.types import Message
from app.telegram_bot.handlers.songs_handler import save_user_link
from app.telegram_bot.handlers.texts_handler import save_lyrics


# 🔁 Պահպանում ենք օգտատերերի վիճակը
user_state = {}

# ✅ Regex checker
def is_youtube_url(text: str) -> bool:
    pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/\S+"
    return re.match(pattern, text) is not None

# 📡 Ուղարկում ենք backend API-ին
def send_to_backend(url: str) -> str:
    try:
        response = requests.post("http://localhost:8000/api/youtube", json={"url": url})
        response.raise_for_status()
        data = response.json()
        return data.get("lyrics", "❌ Couldn't find lyrics.")
    except Exception as e:
        return f"🚫 Error from backend: {e}"

def register(dp: Dispatcher):
    # 🎼 Երբ սեղմում են մենյուից
    @dp.message_handler(lambda msg: msg.text == "🎼 Ստացիր երգի բառերը")
    async def ask_for_link(message: Message):
        user_state[message.from_user.id] = "awaiting_youtube_link"
        await message.answer("📥 Խնդրում եմ ուղարկիր YouTube հղումը՝ երգի բառերը ստանալու համար։")

    # 📩 Երբ ստանում ենք հղումը
    @dp.message_handler()
    async def handle_text(message: Message):
        user_id = message.from_user.id
        text = message.text.strip()

        if user_state.get(user_id) == "awaiting_youtube_link":
            if is_youtube_url(text):
                save_user_link(user_id, text)  # ✅ Հիշում ենք հղումը
                await message.answer("🔎 Վերլուծում եմ YouTube հղումը...")
                lyrics = send_to_backend(text)
                save_lyrics(user_id, text, lyrics)  # ✅ Պահպանում ենք երգի բառերը
                await message.answer(f"🎶 Բառեր:\n\n{lyrics}")
            else:
                await message.answer("❌ Խնդրում եմ ուղարկիր վավեր YouTube հղում։")
            user_state[user_id] = None
