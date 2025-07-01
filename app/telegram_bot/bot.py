# import os
# import logging
# import re
# import requests
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
# from aiogram.utils import executor
# from dotenv import load_dotenv

# # 📥 Load .env
# load_dotenv()
# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# # 🤖 Bot setup
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher(bot)

# # 🎛️ Main Menu Buttons
# main_menu = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton("🎼 Ստացիր երգի բառերը")],
#         [KeyboardButton("🎵 Ուղարկված երգեր")],
#         [KeyboardButton("📝 Անցած տեքստեր")],
#         [KeyboardButton("⬇️ Ներբեռնել երգը")],
#         [KeyboardButton("✍️ Շարունակիր պատմությունը")],
#     ],
#     resize_keyboard=True
# )

# # 🧠 Regex checker
# def is_youtube_url(text: str) -> bool:
#     pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/\S+"
#     return re.match(pattern, text) is not None

# # 📡 Call FastAPI backend
# def send_to_backend(url: str) -> str:
#     try:
#         response = requests.post("http://localhost:8000/api/youtube", json={"url": url})
#         response.raise_for_status()
#         data = response.json()
#         return data.get("lyrics", "❌ Couldn't find lyrics.")
#     except Exception as e:
#         return f"🚫 Error from backend: {e}"

# # 🧠 User state dict
# user_state = {}

# # 🚀 Start command
# @dp.message_handler(commands=["start"])
# async def start_command(message: Message):
#     await message.answer(
#         "🎤 Բարի գալուստ SmartPromptBox Pro բոտ ❗\nԸնտրիր բաժին 👇",
#         reply_markup=main_menu
#     )

# # 🎼 Get lyrics (menu step)
# @dp.message_handler(lambda msg: msg.text == "🎼 Ստացիր երգի բառերը")
# async def ask_for_link(message: Message):
#     user_state[message.from_user.id] = "awaiting_youtube_link"
#     await message.answer("📥 Խնդրում եմ ուղարկիր YouTube հղումը՝ երգի բառերը ստանալու համար։")

# # 🎵 Show sent songs
# @dp.message_handler(lambda msg: msg.text == "🎵 Ուղարկված երգեր")
# async def show_sent_songs(message: Message):
#     await message.answer("📄 Այստեղ կլինեն բոլոր ուղարկված YouTube հղումները։")

# # 📝 Past lyrics
# @dp.message_handler(lambda msg: msg.text == "📝 Անցած տեքստեր")
# async def show_lyrics(message: Message):
#     await message.answer("📚 Այստեղ կլինեն երգերի բառերը՝ յուրաքանչյուրը առանձին։")

# # ⬇️ Download audio/video
# @dp.message_handler(lambda msg: msg.text == "⬇️ Ներբեռնել երգը")
# async def download_song(message: Message):
#     await message.answer("🎶 Ընտրիր երգը՝ ներբեռնելու audio/video տարբերակը։")

# # ✍️ GPT Story continuation
# @dp.message_handler(lambda msg: msg.text == "✍️ Շարունակիր պատմությունը")
# async def continue_story(message: Message):
#     await message.answer("📜 Գրիր պատմության սկիզբը, և ես այն կշարունակեմ 🧠")

# # 📩 Handle all other messages
# @dp.message_handler()
# async def handle_text(message: Message):
#     user_id = message.from_user.id
#     text = message.text.strip()

#     # 🎼 If user is in lyrics mode
#     if user_state.get(user_id) == "awaiting_youtube_link":
#         if is_youtube_url(text):
#             await message.answer("🔎 Վերլուծում եմ YouTube հղումը...")
#             lyrics = send_to_backend(text)
#             await message.answer(f"🎶 Բառեր:\n\n{lyrics}")
#         else:
#             await message.answer("❌ Խնդրում եմ ուղարկիր վավեր YouTube հղում։")
#         user_state[user_id] = None
#         return

#     # 🗨️ Default fallback
#     await message.answer(f"📥 Դու ուղարկեցիր. {text}\n(Օգտվիր մենյուից 👇)")

# # 🏁 Run bot
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     executor.start_polling(dp, skip_updates=True)

# app/telegram_bot/bot.py

import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

from app.telegram_bot.menu import main_menu
from app.telegram_bot.handlers import (
    lyrics_handler,
    songs_handler,
    texts_handler,
    download_handler,
    story_handler,
    fallback,
    send_pdf_handler,
)

# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ✅ /start հրամանի հենդլեր
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer("🎤 Բարի գալուստ SmartPromptBox Pro! Ընտրիր բաժին մենյուից 👇", reply_markup=main_menu)

# Register all handlers
lyrics_handler.register(dp)
songs_handler.register(dp)
texts_handler.register(dp)
download_handler.register(dp)
story_handler.register(dp)
fallback.register(dp)
send_pdf_handler.register(dp)

# Start polling
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
