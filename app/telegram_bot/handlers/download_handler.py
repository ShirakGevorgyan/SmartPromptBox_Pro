# app/telegram_bot/handlers/download_handler.py

import os
import yt_dlp
from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InputFile
from app.telegram_bot.handlers.songs_handler import user_links

download_state = {}

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_audio(url: str, filename: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, filename)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

def download_video(url: str, filename: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, filename)
    ydl_opts = {
        "format": "mp4",
        "outtmpl": output_path,
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

def register(dp: Dispatcher):
    @dp.message_handler(lambda msg: msg.text == "⬇️ Ներբեռնել երգը")
    async def choose_song(message: Message):
        user_id = message.from_user.id
        links = user_links.get(user_id, [])

        if not links:
            await message.answer("📭 Դու դեռ ոչ մի հղում չես ուղարկել։")
        else:
            buttons = [[KeyboardButton(link)] for link in links]
            keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
            download_state[user_id] = {"step": "select_link"}
            await message.answer("⬇️ Ընտրիր հղումը՝ ներբեռնելու համար։", reply_markup=keyboard)

    @dp.message_handler()
    async def handle_download_steps(message: Message):
        user_id = message.from_user.id
        state = download_state.get(user_id)

        if not state:
            return

        # Քայլ 1․ ընտրել հղումը
        if state["step"] == "select_link":
            link = message.text.strip()
            if link not in user_links.get(user_id, []):
                await message.answer("❌ Սա քո ուղարկած հղումներից չէ։")
                return
            download_state[user_id] = {
                "step": "select_type",
                "link": link
            }
            buttons = [[KeyboardButton("🎧 Audio"), KeyboardButton("🎥 Video")]]
            keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
            await message.answer("🔽 Որ ձևաչափով ես ուզում ներբեռնել?", reply_markup=keyboard)
            return

        # Քայլ 2․ ընտրել տեսակը
        if state["step"] == "select_type":
            choice = message.text.strip().lower()
            link = state["link"]

            await message.answer("⏳ Ներբեռնում եմ, սպասիր...")

            try:
                filename = f"{user_id}_{int(message.date.timestamp())}"

                if "audio" in choice:
                    path = download_audio(link, filename + ".mp3")
                    await message.answer_audio(InputFile(path), caption="🎶 Ահա քո երգը (audio)")
                elif "video" in choice:
                    path = download_video(link, filename + ".mp4")
                    await message.answer_video(InputFile(path), caption="🎬 Ահա քո երգը (video)")
                else:
                    await message.answer("❌ Ընտրությունը չհասկացա։")

                os.remove(path)

            except Exception as e:
                await message.answer(f"❌ Չհաջողվեց ներբեռնել. {e}")

            download_state[user_id] = None
