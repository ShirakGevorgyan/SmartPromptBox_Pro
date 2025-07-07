from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import asyncio
import os
from app.utils.youtube_downloader import download_audio, download_video

class DownloadStates(StatesGroup):
    waiting_for_url = State()
    choosing_format = State()
    choosing_quality = State()

def register(dp: Dispatcher):
    dp.register_message_handler(start_download, lambda m: m.text == "⬇️ Ներբեռնել երգը", state="*")
    dp.register_message_handler(receive_url, state=DownloadStates.waiting_for_url)
    dp.register_message_handler(choose_format, state=DownloadStates.choosing_format)
    dp.register_message_handler(choose_quality, state=DownloadStates.choosing_quality)
    dp.register_message_handler(restart_download, lambda m: m.text == "🔁 Նոր հղում ուղարկել", state="*")

async def start_download(message: Message, state: FSMContext):
    await message.answer("📎 Ուղարկիր YouTube հղումը:")
    await DownloadStates.waiting_for_url.set()

async def receive_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text)

    format_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("🎵 Աուդիո"), KeyboardButton("🎥 Վիդեո")]],
        resize_keyboard=True
    )
    await message.answer("📥 Որ տարբերակով ես ուզում ներբեռնել?", reply_markup=format_keyboard)
    await DownloadStates.choosing_format.set()

async def choose_format(message: Message, state: FSMContext):
    user_choice = message.text
    await state.update_data(format=user_choice)

    if user_choice == "🎥 Վիդեո":
        quality_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("🔺 720p"), KeyboardButton("🔹 480p")],
                [KeyboardButton("🔸 360p"), KeyboardButton("🔻 240p")]
            ],
            resize_keyboard=True
        )
        await message.answer("📺 Ընտրիր որակը:", reply_markup=quality_keyboard)
        await DownloadStates.choosing_quality.set()
    else:
        data = await state.get_data()
        url = data["url"]
        await message.answer("⏳ Ներբեռնում եմ աուդիոն․․․", reply_markup=ReplyKeyboardRemove())
        file_path = await asyncio.to_thread(download_audio, url)

        if not os.path.exists(file_path):
            await message.answer("❌ Աուդիոն ներբեռնել չհաջողվեց։")
            await state.finish()
            return

        clean_name = os.path.splitext(os.path.basename(file_path))[0]
        document = InputFile(file_path, filename=f"{clean_name}.mp3")
        await message.answer_document(document, caption=clean_name)
        os.remove(file_path)

        await message.answer(
            "✅ Ներբեռնումը ավարտված է։\nՈւղարկիր նոր հղում կամ սեղմիր «🔁 Նոր հղում ուղարկել»:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton("🔁 Նոր հղում ուղարկել")]],
                resize_keyboard=True,
                one_time_keyboard=True,
            )
        )
        await state.finish()

async def choose_quality(message: Message, state: FSMContext):
    data = await state.get_data()
    url = data["url"]
    quality = message.text.replace("🔺", "").replace("🔹", "").replace("🔸", "").replace("🔻", "").strip()

    await message.answer(f"⏳ Ներբեռնում եմ վիդեոն՝ {quality} որակով․․․", reply_markup=ReplyKeyboardRemove())
    file_path = await asyncio.to_thread(download_video, url, quality)

    if not os.path.exists(file_path):
        await message.answer("❌ Վիդեոն ներբեռնել չհաջողվեց։")
        await state.finish()
        return

    clean_name = os.path.splitext(os.path.basename(file_path))[0]
    document = InputFile(file_path, filename=f"{clean_name}.mp4")
    await message.answer_document(document, caption=clean_name)
    os.remove(file_path)

    await message.answer(
        "✅ Ներբեռնումը ավարտված է։\nՈւզում ես նոր հղում ուղարկել? Սեղմիր «🔁 Նոր հղում ուղարկել»:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("🔁 Նոր հղում ուղարկել")]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    )
    await state.finish()

async def restart_download(message: Message, state: FSMContext):
    await message.answer("📎 Ուղարկիր YouTube հղումը:")
    await DownloadStates.waiting_for_url.set()
