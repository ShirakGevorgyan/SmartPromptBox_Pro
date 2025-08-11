import os
import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart
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

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

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

    dp.include_router(gpt_memory_chat_handler.router)
    dp.include_router(mood_handler.router)
    dp.include_router(random_songs_handler.router)
    dp.include_router(series_menu_handler.router)
    dp.include_router(movie_menu_handler.router)
    dp.include_router(img_handler.router)

    dp.message.register(start_command_handler, CommandStart())
    return dp

def make_bot(token: str) -> Bot:
    client_timeout = aiohttp.ClientTimeout(
        total=70,
        connect=10,
        sock_read=60,
    )
    session = AiohttpSession(timeout=client_timeout)
    return Bot(token=token, session=session, parse_mode="HTML")

async def main():
    logging.basicConfig(level=logging.INFO)

    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN env var is missing")

    dp = build_dispatcher()
    bot = make_bot(BOT_TOKEN)

    backoff = 1
    while True:
        try:
            await dp.start_polling(bot, polling_timeout=50)
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.warning("Polling network error: %r. Retry in %ss", e, backoff)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30)
            continue
        except Exception as e:
            logging.exception("Unexpected polling crash: %r", e)
            await asyncio.sleep(5)
            continue
        finally:
            backoff = 1

if __name__ == "__main__":
    asyncio.run(main())
