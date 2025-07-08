from aiogram import Router
from aiogram.types import Message
from app.telegram_bot.menu import song_menu

router = Router()

# 🎵 Songs բաժնի բացում (հուսալի՝ text-based ստուգում)
@router.message(lambda message: message.text and "🎵 Երգեր" in message.text)
async def open_song_menu(message: Message):
    await message.answer("🎶 Երգերի մենյուն բացվեց!", reply_markup=song_menu)
