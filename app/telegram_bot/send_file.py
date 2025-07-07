# app/telegram_bot/send_file.py

import os
from aiogram import Bot

TEMP_DIR = "app/temp"

async def send_lyrics_file(bot: Bot, chat_id: int, filename: str):
    """
    Ուղարկում է երգի բառերի PDF ֆայլը Telegram օգտատիրոջը
    """
    pdf_path = os.path.join(TEMP_DIR, f"{filename}.pdf")
    if not os.path.exists(pdf_path):
        await bot.send_message(chat_id, "❌ Ֆայլը չի գտնվել։")
        return

    await bot.send_document(chat_id, open(pdf_path, "rb"))
