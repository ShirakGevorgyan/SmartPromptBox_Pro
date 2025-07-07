import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # ✅ Ավելացվել է FSM-ի համար
from dotenv import load_dotenv

from app.telegram_bot.menu import main_menu
from app.telegram_bot.handlers import (
    lyrics_handler,
    songs_handler,
    texts_handler,
    download_handler,
    story_handler,
    fallback,
    send_pdf_handler,
)

# ✅ Բեռնում ենք .env ֆայլից TOKEN-ը
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Ստեղծում ենք Bot և Dispatcher FSM-ով
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()              # ⬅️ FSM հիշողություն
dp = Dispatcher(bot, storage=storage)  # ⬅️ Dispatcher-ը աշխատում է FSM պահեստով

# ✅ /start հրամանի հենդլեր
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer("🎤 Բարի գալուստ SmartPromptBox Pro! Ընտրիր բաժին մենյուից 👇", reply_markup=main_menu)

# ✅ Գրանցում ենք բոլոր handler-ները
lyrics_handler.register(dp)
songs_handler.register(dp)
texts_handler.register(dp)
download_handler.register(dp)  # ⬅️ Սա արդեն FSM է պահանջում
story_handler.register(dp)
fallback.register(dp)
send_pdf_handler.register(dp)

# ✅ Սկսում ենք բոտի աշխատանքը
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
