from datetime import timedelta
import time
import platform
import aiogram
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app import meta

router = Router(name="misc_commands")


@router.message(Command("ping"))
async def ping(m: Message):
    await m.answer("pong 🏓")


@router.message(Command("id"))
async def whoami(m: Message):
    uid = m.from_user.id if m.from_user else "?"
    cid = m.chat.id if m.chat else "?"
    await m.answer(
        f"🪪 <b>User ID:</b> <code>{uid}</code>\n💬 <b>Chat ID:</b> <code>{cid}</code>",
        parse_mode="HTML",
    )


@router.message(Command("about"))
async def about(m: Message):
    uptime = timedelta(seconds=int(time.time() - meta.STARTED_AT))
    await m.answer(
        (
            f"🤖 <b>{meta.BOT_NAME}</b>\n"
            f"📦 Version: <code>{meta.BOT_VERSION}</code>\n"
            f"⏱️ Uptime: <code>{uptime}</code>\n"
            f"🐍 Python: <code>{platform.python_version()}</code>\n"
            f"📚 aiogram: <code>{aiogram.__version__}</code>\n"
        ),
    )


@router.message(Command("help"))
async def help_cmd(m: Message):
    await m.answer(
        (
            "<b>Օգտագործման արագ ուղեցույց</b>\n\n"
            "• /start — բացել գլխավոր մենյուն\n"
            "• 🧠 Mood Assistant — ընտրի՛ր ինչպես ես, բերեմ խորհուրդներ (երգ/ֆիլմ/գործողություն)\n"
            "• 🎬 Ֆիլմեր և Սերիալներ — ընտրի՛ր ժանր, տարին, ռեյթինգը կամ խնդրի՛ր պատահական\n"
            "• 🎵 Երգեր — ըստ տրամադրության, ժանրի, կամ պատահական\n"
            "• 🎨 Նկար գեներացիա — գրի՛ր հուշում (օր. «քաղաք գիշերը, նեոն»), ուղարկեմ գեներացված նկար\n"
            "• ⭐️ Խոսիր ինձ հետ — ազատ զրույց Bot-ի հետ\n\n"
            "<b>Հրամաններ</b>\n"
            "/help · /about · /ping · /id\n\n"
            "<i>Հուշում:</i> Միշտ կարող ես վերադառնալ մենյու՝ «⤴️ Գլխավոր մենյու» կոճակով։"
        ),
    )
