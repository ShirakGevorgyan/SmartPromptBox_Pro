# app/telegram_bot/menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🎛️ Գլխավոր մենյուի կառուցում
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🎼 Ստացիր երգի բառերը")],
        [KeyboardButton("🎵 Ուղարկված երգեր")],
        [KeyboardButton("📝 Անցած տեքստեր")],
        [KeyboardButton("⬇️ Ներբեռնել երգը")],
        [KeyboardButton("✍️ Շարունակիր պատմությունը")],
    ],
    resize_keyboard=True
)
