# app/telegram_bot/handlers/lyrics_handler.py

from aiogram import types, Dispatcher
from app.utils.lyrics_generator import generate_lyrics
from app.telegram_bot.send_file import send_lyrics_file

# Պահելու համար user-ի վերջին հղումը
temp_links = {}

async def ask_for_link(message: types.Message):
    await message.reply("📥 Ուղարկիր YouTube հղումը և կբերեմ բառերը ✨")

async def lyrics_from_text(message: types.Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("❌ Խնդրում եմ ուղարկեք վավեր YouTube հղում։")
        return

    await message.reply("🔍 Վերլուծում եմ YouTube հղումը…")

    try:
        from yt_dlp import YoutubeDL
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'no_warnings': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "Unknown")
            artist = info.get("uploader", "Unknown")

        # Ստանում ենք բառերը բոլոր ճանապարհներով (GPT→Genius→Whisper)
        lyrics = generate_lyrics(title, artist, youtube_url=url)

        await message.reply("📄 Ահա քո երգի բառերը PDF ֆայլով ⬇️")
        filename = f"{title}_{artist}".replace(" ", "_")
        await send_lyrics_file(message.bot, message.chat.id, filename)

    except Exception as e:
        await message.reply(f"❌ Սխալ տեղի ունեցավ։\n{str(e)}")


def register(dp: Dispatcher):
    dp.register_message_handler(ask_for_link, lambda m: m.text == "🎼 Ստացիր երգի բառերը")
    dp.register_message_handler(lyrics_from_text, regexp=r"https?://(www\.)?(youtube|youtu)\.")
