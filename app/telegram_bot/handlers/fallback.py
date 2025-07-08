from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def handle_unknown(message: Message):
    await message.answer(
        "🤔 Չհասկացա ինչ ես փորձում անել։\n"
        "📌 Խնդրում եմ օգտվիր ներքևի մենյուից կամ ուղարկիր վավեր հարցում։"
    )
