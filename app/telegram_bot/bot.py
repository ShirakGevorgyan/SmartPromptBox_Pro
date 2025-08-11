import os
import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.telegram_bot.handlers import misc_commands
from app.telegram_bot.middlewares.logging import LogUpdate
from app.telegram_bot.middlewares.errors import CatchAllErrors

from dotenv import load_dotenv

from app.telegram_bot.handlers import (
    random_songs_handler,
    gpt_memory_chat_handler,
    movie_menu_handler,
    series_menu_handler,
    img_handler,
    mood_handler,
)
from app.telegram_bot.menu import main_menu
from app.utils.logging_config import setup_logging

setup_logging()
load_dotenv()

BOT_TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()

async def start_command_handler(message: Message):
    await message.answer(
        "👋 Բարի գալուստ SmartPromptBox Pro բոտ! \n\n"
        "Այս բոտը կօգնի քեզ գտնել լավագույն երգերը, ֆիլմերը և ստեղծել յուրահատուկ նկարներ։\n\n"
        "Ընտրիր ցանկալի գործողությունը՝ օգտագործելով ներքևի մենյուն։",
        reply_markup=main_menu,
    )

def build_dispatcher() -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    dp.message.middleware(CatchAllErrors())
    dp.message.middleware(LogUpdate())
    
    dp.include_router(gpt_memory_chat_handler.router)
    dp.include_router(mood_handler.router)
    dp.include_router(random_songs_handler.router)
    dp.include_router(series_menu_handler.router)
    dp.include_router(movie_menu_handler.router)
    dp.include_router(img_handler.router)
    
    dp.include_router(misc_commands.router)
    
    dp.message.register(start_command_handler, CommandStart())
    return dp

def make_bot(token: str) -> Bot:
    # ⚠️ Այստեղ էր խնդիրը: AiohttpSession-ին պետք ա տալ ՑԱԾՐԱԹՎԱՅԻՆ timeout, ոչ թե ClientTimeout օբյեկտ
    session = AiohttpSession(timeout=60)  # seconds
    return Bot(
        token=token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN env var is missing")

    dp = build_dispatcher()
    bot = make_bot(BOT_TOKEN)

    backoff = 1
    while True:
        try:
            # numeric request_timeout → այլևս չի լինի `ClientTimeout + int`
            await dp.start_polling(bot, polling_timeout=50, request_timeout=120)
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.warning("Polling network error: %r. Retry in %ss", e, backoff)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30)
        except Exception as e:
            logging.exception("Unexpected polling crash: %r", e)
            await asyncio.sleep(5)
        else:
            backoff = 1  # եթե երբևէ դադարեց՝ reset backoff

if __name__ == "__main__":
    asyncio.run(main())
