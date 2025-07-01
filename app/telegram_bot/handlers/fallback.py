# app/telegram_bot/handlers/fallback.py

from aiogram import Dispatcher
from aiogram.types import Message

def register(dp: Dispatcher):
    @dp.message_handler()
    async def handle_unknown(message: Message):
        await message.answer(
            "🤔 Չհասկացա ինչ ես փորձում անել։\n"
            "📌 Խնդրում եմ օգտվիր ներքևի մենյուից կամ ուղարկիր վավեր հարցում։"
        )
