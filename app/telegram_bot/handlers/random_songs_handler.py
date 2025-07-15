from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.llm.mood_inferencer import generate_songs_random
from app.telegram_bot.menu import random_song_menu, main_menu
from app.utils.youtube_downloader import download_audio
from app.llm.clean_title import clean_song_title_llm
import os

router = Router()

@router.message(F.text == "🔀 Պատահական երգ")
async def random_song_handler(message: Message, state: FSMContext):
    await message.answer("🎲 Սպասիր, գտնում եմ պատահական երգ…")

    songs = generate_songs_random()
    if not songs:
        await message.answer("❌ Չհաջողվեց գտնել երգ։ Փորձիր նորից 😢")
        return

    await send_song_buttons(songs, message, state)


# ✅ Ցուցադրում է երգը՝ download կոճակով
async def send_song_buttons(songs: list[dict], message: Message, state: FSMContext):
    await state.update_data(songs_for_download=songs)  # store full list in FSM

    for idx, song in enumerate(songs):
        title = song["title"]
        artist = song["artist"]
        description = song["description"]
        youtube_url = song["youtube"]

        text = (
            f"<b>{title}</b> — <i>{artist}</i>\n"
            f"📎 {description}"
        )
        callback_data = f"download_{idx}"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 YouTube", url=youtube_url)],
            [InlineKeyboardButton(text="⬇️ Ներբեռնել", callback_data=callback_data)]
        ])
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


# ✅ Callback ֆունկցիա՝ ներբեռնման համար
@router.callback_query(F.data.startswith("download_"))
async def handle_download_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer("⬇️ Ներբեռնում եմ...")

    try:
        index = int(callback.data.split("_")[1])
        data = await state.get_data()
        songs = data.get("songs_for_download", [])

        if index < 0 or index >= len(songs):
            await callback.message.answer("❌ Սխալ ինդեքս։")
            return

        song = songs[index]
        youtube_url = song["youtube"]
        title = song["title"]

        clean_name = clean_song_title_llm(title)
        file_path = download_audio(youtube_url, filename=clean_name)
        audio = FSInputFile(file_path)

        await callback.message.answer_audio(audio, caption=f"🎵 {clean_name}")
        os.remove(file_path)
        await callback.message.delete()

        # ✅ Վերջում ավելացնենք reply մենյուն
        await callback.message.answer("Ընտրիր՝", reply_markup=random_song_menu)

    except Exception as e:
        print("❌ Download error:", e)
        await callback.message.answer("Չհաջողվեց ներբեռնել երգը։")


# ✅ Նոր պատահական երգ
@router.message(F.text == "🔁 Նոր պատահական երգ")
async def new_random_song_handler(message: Message, state: FSMContext):
    await random_song_handler(message, state)


# ✅ Վերադարձ գլխավոր մենյու
@router.message(F.text == "🔝 Վերադառնալ գլխավոր մենյու")
async def back_to_main_menu(message: Message):
    await message.answer("🎼 Վերադարձ գլխավոր մենյու։", reply_markup=main_menu)
