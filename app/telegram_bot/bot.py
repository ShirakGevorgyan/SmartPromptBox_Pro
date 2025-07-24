import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# ✅ Ռաութերներ
from app.telegram_bot.handlers import mood_handler



from app.telegram_bot.handlers import (
    song_menu_handler,
    random_songs_handler,
    gpt_memory_chat_handler,
    movie_menu_handler,
    series_menu_handler,
    img_handler,
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
    dp.include_router(gpt_memory_chat_handler.router)
    dp.include_router(song_menu_handler.router)
    dp.include_router(mood_handler.router)
    dp.include_router(random_songs_handler.router)
    dp.include_router(series_menu_handler.router)
    dp.include_router(movie_menu_handler.router)
    dp.include_router(img_handler.router)

    # ✅ /start command գրանցում
    dp.message.register(start_command_handler, CommandStart())

    # ▶️ Սկսում ենք polling-ը
    await dp.start_polling(bot)

# 🔁 Բոտի գործարկում
if __name__ == "__main__":
    asyncio.run(main())