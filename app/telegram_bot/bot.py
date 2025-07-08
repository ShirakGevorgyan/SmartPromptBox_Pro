import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# ✅ Ռաութերներ
from app.telegram_bot.routers import mood_router

from app.telegram_bot.handlers import (
    # lyrics_handler,
    songs_handler,
    download_handler,
    story_handler,
    fallback,
    send_pdf_handler,
    song_menu_handler,  # ✅ ավելացված՝ Երգերի մենյուի կառավարում
)

# ✅ Մենյուներ
from app.telegram_bot.menu import (
    main_menu,
)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 🎯 Start հրամանի ֆունկցիա
async def start_command_handler(message: Message):
    await message.answer(
        "👋 Բարի գալուստ SmartPromptBox Pro բոտ! \n\n"
        "Այս բոտը կօգնի քեզ գտնել լավագույն երգերը, ֆիլմերը և ստեղծել յուրահատուկ նկարներ։\n\n"
        "Ընտրիր ցանկալի գործողությունը՝ օգտագործելով ներքևի մենյուն։",
        reply_markup=main_menu
    )

# 🧠 Գլխավոր async ֆունկցիա
async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # ✅ Ռաութերների գրանցում (song_menu_handler-ը ամենավերևում)
    dp.include_router(song_menu_handler.router)
    dp.include_router(mood_router.router)
    # dp.include_router(lyrics_handler.router)
    dp.include_router(songs_handler.router)
    dp.include_router(download_handler.router)
    dp.include_router(story_handler.router)
    dp.include_router(fallback.router)
    dp.include_router(send_pdf_handler.router)

    # ✅ /start command գրանցում
    dp.message.register(start_command_handler, CommandStart())

    # ▶️ Սկսում ենք polling-ը
    await dp.start_polling(bot)

# 🔁 Բոտի գործարկում
if __name__ == "__main__":
    asyncio.run(main())