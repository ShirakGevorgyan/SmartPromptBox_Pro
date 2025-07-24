from aiogram import Router, F
from aiogram.types import Message#, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton#, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.llm.mood_inferencer import generate_songs_random
from app.telegram_bot.menu import main_menu#,  random_song_menu, main_menu
# from app.utils.youtube_downloader import download_audio
# from app.llm.clean_title import clean_song_title_llm
# import os

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
        # callback_data = f"download_{idx}"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 YouTube", url=youtube_url)],
            # [InlineKeyboardButton(text="⬇️ Ներբեռնել", callback_data=callback_data)]
        ])
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


# ✅ Նոր պատահական երգ
@router.message(F.text == "🔁 Նոր պատահական երգ")
async def new_random_song_handler(message: Message, state: FSMContext):
    await random_song_handler(message, state)


# ✅ Վերադարձ գլխավոր մենյու
@router.message(F.text == "🔝 Վերադառնալ գլխավոր մենյու")
async def back_to_main_menu(message: Message):
    await message.answer("🎼 Վերադարձ գլխավոր մենյու։", reply_markup=main_menu)
