from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.llm.mood_inferencer import generate_songs_random
from app.llm.song_llm import (
    generate_songs_by_genre,
    generate_songs_by_description,
    generate_top_songs_by_artist
)
from app.telegram_bot.menu import main_menu, genre_menu, song_menu
router = Router()


class SongStates(StatesGroup):
    waiting_for_genre = State()
    waiting_for_description = State()
    waiting_for_artist = State()


# GENRE_MAP = {
#     "🎸 Ռոք": "Rock",
#     "🎹 Ջազ": "Jazz",
#     "🎤 Ռեփ": "Rap",
#     "🎶 Փոփ": "Pop",
#     "💃 Լատինո": "Latino",
#     "🎻 Կլասիկ": "Classical",
#     "🏞 Ֆոլք": "Folk",
#     "🎼 Էլեկտրոնային": "Electronic",
#     "🔥 Մետալ": "Metal",
#     "🎷 Ֆանկ": "Funk",
# }

@router.message(F.text == "🔀 Պատահական երգ")
async def random_song_handler(message: Message, state: FSMContext):
    await message.answer("🎲 Սպասիր, գտնում եմ պատահական երգ…")

    songs = generate_songs_random()
    if not songs:
        await message.answer("❌ Չհաջողվեց գտնել երգ։ Փորձիր նորից 😢")
        return

    await send_song_buttons(songs, message, state)


async def send_song_buttons(songs: list[dict], message: Message, state: FSMContext):
    await state.update_data(songs_for_download=songs)

    for song in songs:
        title = song["title"]
        artist = song["artist"]
        description = song["description"]
        youtube_url = song["youtube"]

        text = f"<b>{title}</b> — <i>{artist}</i>\n📎 {description}"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 YouTube", url=youtube_url)],
        ])
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.message(F.text == "🔁 Նոր պատահական երգ")
async def new_random_song_handler(message: Message, state: FSMContext):
    await random_song_handler(message, state)



@router.message(F.text == "🔝 Վերադառնալ գլխավոր մենյու")
async def back_to_main_menu(message: Message):
    await message.answer("🎼 Վերադարձ գլխավոր մենյու։", reply_markup=main_menu)
    
    
@router.message(F.text == "🔙 Վերադառնալ Երգեր մենյու")
async def back_to_song_menu(message: Message):
    await message.answer("🎼 Վերադարձ Երգեր մենյու։", reply_markup=song_menu)



@router.message(F.text == "🎧 Ըստ ոճի")
async def ask_for_genre(message: Message, state: FSMContext):
    await message.answer("🎧 Խնդրում եմ ընտրիր կամ գրիր երաժշտական ոճը։", reply_markup=genre_menu)
    await state.set_state(SongStates.waiting_for_genre)


@router.message(SongStates.waiting_for_genre)
async def handle_genre_input(message: Message, state: FSMContext):
    genre = message.text.strip("🎸🎹🎤🎶💃🎻🏞🎼🔥🎷 ")
    # selected = message.text.strip()
    # genre = GENRE_MAP.get(selected)

    if not genre:
        await message.answer("❗️ Չճանաչված ժանր։ Փորձիր նորից ընտրել ցանկից։", reply_markup=genre_menu)
        return

    await message.answer(f"🎧 Որոնում եմ {genre} ոճի երգեր…")

    songs = generate_songs_by_genre(genre)
    if not songs:
        await message.answer("❌ Չհաջողվեց գտնել երգեր։")
        return

    await message.answer("🎧 Ահա քո երգերը՝")
    await send_song_buttons(songs, message, state)
    await message.answer("🤖 Հաջորդը ի՞նչ կուզես անենք։ Նոր ոճ ընտրիր կամ վերադարձիր մենյուին։", reply_markup=genre_menu)
    await state.clear()
    await state.set_state(SongStates.waiting_for_genre)


@router.message(F.text == "📝 Ըստ նկարագրության")
async def ask_for_description(message: Message, state: FSMContext):
    await message.answer("📄 Գրիր երգի կամ տրամադրության նկարագրությունը։")
    await state.set_state(SongStates.waiting_for_description)


@router.message(SongStates.waiting_for_description)
async def handle_description_input(message: Message, state: FSMContext):
    description = message.text
    await message.answer("🔍 Որոնում եմ նկարագրությանը համապատասխան երգեր…")

    songs = generate_songs_by_description(description)
    if not songs:
        await message.answer("❌ Չհաջողվեց գտնել երգեր։")
        return
    await message.answer("🎧 Ահա քո երգը՝")
    await send_song_buttons(songs, message, state)
    await message.answer("🤖 Հաջորդը ի՞նչ կուզես անենք։", reply_markup=song_menu)
    await state.clear()
    await state.set_state(SongStates.waiting_for_description)


@router.message(F.text == "🧑‍🎤 Արտիստի լավագույն երգերը")
async def ask_for_artist_name(message: Message, state: FSMContext):
    await message.answer("🧑‍🎤 Գրիր արտիստի կամ խմբի անունը։")
    await state.set_state(SongStates.waiting_for_artist)


@router.message(SongStates.waiting_for_artist)
async def handle_artist_input(message: Message, state: FSMContext):
    artist = message.text
    await message.answer(f"🔍 Որոնում եմ {artist}-ի լավագույն երգերը…")

    songs = generate_top_songs_by_artist(artist)
    if not songs:
        await message.answer("❌ Չհաջողվեց գտնել այդ արտիստի երգերը։")
        return
    await message.answer("🎧 Ահա քո երգերը՝")
    await send_song_buttons(songs, message, state)
    await message.answer("🤖 Հաջորդը ի՞նչ կուզես անենք։", reply_markup=song_menu)
    await state.clear()
    await state.set_state(SongStates.waiting_for_artist)

# 🎵 Songs բաժնի բացում (հուսալի՝ text-based ստուգում)
@router.message(lambda message: message.text and "🎵 Երգեր" in message.text)
async def open_song_menu(message: Message):
    await message.answer("🎶 Երգերի մենյուն բացվեց!", reply_markup=song_menu)
