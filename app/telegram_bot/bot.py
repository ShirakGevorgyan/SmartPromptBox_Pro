import os
import logging
import asyncio
import aiohttp

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, BotCommand

from dotenv import load_dotenv

from app.telegram_bot.handlers import (
    random_songs_handler,
    gpt_memory_chat_handler,
    movie_menu_handler,
    series_menu_handler,
    img_handler,
    mood_handler,
    misc_commands,
)
from app.telegram_bot.menu import main_menu
from app.telegram_bot.middlewares.logging import LogUpdate
from app.telegram_bot.middlewares.errors import CatchAllErrors
from app.telegram_bot.middlewares.request_id import RequestId

from app.utils.logging_config import setup_logging
from app.data.database import init_db

setup_logging()
load_dotenv()
BOT_TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()

async def start_command_handler(message: Message):
    await message.answer(
        (
            "👋 Բարի գալուստ <b>SmartPromptBox Pro</b>։\n"
            "Ընտրիր բաժին կոճակներից կամ գրիր հրաման (/help)։\n\n"
            "• 🧠 Mood Assistant — տրամադրությունից խորհուրդներ\n"
            "• 🎬 Ֆիլմեր և Սերիալներ — ինչ դիտել այսօր\n"
            "• 🎵 Երգեր — առաջարկներ/պատահական\n"
            "• 🎨 Նկար գեներացիա — գրիր հուշում, գեներացնենք\n"
            "• ⭐ Խոսիր ինձ հետ — ազատ չաթ"
        ),
        reply_markup=main_menu,
    )

def build_dispatcher() -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # middlewares (պատվերով հերթականությամբ)
    dp.message.middleware(RequestId())
    dp.message.middleware(CatchAllErrors())
    dp.message.middleware(LogUpdate())

    # routers
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
    # INT timeout՝ որպեսզի aiogram-ը կարողանա գումարել polling_timeout-ին
    session = AiohttpSession(timeout=60)
    return Bot(
        token=token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN env var is missing")

    # ✅ DB schema միշտ լինի ստեղծված
    init_db()

    dp = build_dispatcher()
    bot = make_bot(BOT_TOKEN)

    # մեկ instance only + մաքրում
    await bot.delete_webhook(drop_pending_updates=True)

    # UI commands
    try:
        await bot.set_my_commands(
            commands=[
                BotCommand(command="start", description="Գլխավոր մենյու"),
                BotCommand(command="help",  description="Օգնություն / օգտագործում"),
                BotCommand(command="about", description="Անուն, վերսիա, uptime"),
                BotCommand(command="ping",  description="Արագ ստուգում"),
                BotCommand(command="id",    description="User/Chat ID-ներ"),
            ]
        )
    except Exception as e:
        logging.warning("set_my_commands failed: %r", e)

    backoff = 1
    while True:
        try:
            # request_timeout-ը գումարվում է bot.session.timeout-ին => ապահով է, քանի որ session.timeout=60 (int)
            await dp.start_polling(bot, polling_timeout=50, request_timeout=120)
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.warning("Polling network error: %r. Retry in %ss", e, backoff)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30)
        except Exception as e:
            logging.exception("Unexpected polling crash: %r", e)
            await asyncio.sleep(5)
        else:
            backoff = 1

if __name__ == "__main__":
    asyncio.run(main())
