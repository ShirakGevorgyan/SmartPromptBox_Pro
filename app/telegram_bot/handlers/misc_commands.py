from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="misc_commands")

@router.message(Command("ping"))
async def ping(m: Message):
    await m.answer("pong 🏓")

@router.message(Command("help"))
async def help_cmd(m: Message):
    await m.answer(
        "Հրամաններ՝\n"
        "• /start — գլխավոր մենյու\n"
        "• /help — այս օգնությունը\n"
        "• /ping — արագ ստուգում\n\n"
        "Բոտը կարող է՝ տրամադրել երգերի/ֆիլմերի առաջարկներ, mood-ից կախված խորհուրդներ "
        "և նկարների գեներացիա։"
    )
