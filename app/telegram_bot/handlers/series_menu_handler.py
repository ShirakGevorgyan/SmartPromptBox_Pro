from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

from app.telegram_bot.handlers.movie_menu_handler import split_movies
from app.telegram_bot.menu import (
    series_menu,
    film_and_series_menu,
    main_menu,
    series_genre_menu,
)
from app.llm.series_picker import (
    get_random_series_llm,
    suggest_series_by_description_llm,
    get_series_details_by_name_llm,
    get_top_10_series_llm,
    get_series_by_genre_llm
)

router = Router()


class SeriesStates(StatesGroup):
    waiting_for_description = State()
    waiting_for_series_name = State()
    waiting_for_genre = State()


SERIES_GENRE_MAP = {
    "🎭 Դրամա": "Drama",
    "😂 Կատակերգություն": "Comedy",
    "🚀 Գիտաֆանտաստիկա": "Science Fiction",
    "🧙 Ֆանտազիա": "Fantasy",
    "😱 Սարսափ": "Horror",
    "🕵️ Թրիլեր": "Thriller",
    "💘 Ռոմանտիկա": "Romance",
    "👨‍👩‍👧 Ընտանեկան": "Family",
    "🎬 Պատմական": "Historical",
    "🧩 Միստիկա": "Mystery"
}

def extract_links_from_text(text: str):
    trailer_match = re.search(r"Տրեյլեր՝ \[.*?\]\((.*?)\)", text)
    watch_match = re.search(r"Դիտելու հղում՝ \[.*?\]\((.*?)\)", text)
    return (
        trailer_match.group(1) if trailer_match else None,
        watch_match.group(1) if watch_match else None
    )

def clean_llm_text(text: str) -> str:
    lines = text.strip().split("\n")
    cleaned_lines = [line for line in lines if not line.startswith("▶️ Տրեյլեր") and not line.startswith("🎞️ Դիտելու հղում")]
    return "\n".join(cleaned_lines)

async def send_long_message(message: Message, full_text: str, reply_markup=None):
    max_length = 4096
    chunks = [full_text[i:i + max_length] for i in range(0, len(full_text), max_length)]
    for i, chunk in enumerate(chunks):
        markup = reply_markup if i == len(chunks) - 1 else None
        await message.answer(chunk, reply_markup=markup)



@router.message(F.text.func(lambda text: text.strip() == "🎬 Ֆիլմեր և Սերիալներ"))
async def open_film_and_series_menu(message: Message):
    await message.answer("🎥 Ընտրիր՝ ֆիլմեր թե սերիալներ։", reply_markup=film_and_series_menu)

@router.message(F.text == "📺 Սերիալներ")
async def show_series_menu(message: Message):
    await message.answer("📺 Ընտրիր գործողությունը սերիալների համար։", reply_markup=series_menu)

@router.message(F.text == "🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")
async def back_to_film_series_menu(message: Message):
    await message.answer("📚 Վերադարձիր Ֆիլմերի և Սերիալների ընտրությանը։", reply_markup=film_and_series_menu)

@router.message(F.text == "🔝 Վերադառնալ գլխավոր մենյու")
async def back_to_main_menu(message: Message):
    await message.answer("🏠 Գլխավոր մենյու", reply_markup=main_menu)



@router.message(F.text.in_({"🎲 Պատահական սերիալ", "🔁 Նոր պատահական սերիալ"}))
async def send_random_series(message: Message):
    await message.answer("🎯 Ընտրում եմ պատահական սերիալ... ⏳")
    result = get_random_series_llm()
    trailer_url, watch_url = extract_links_from_text(result)
    cleaned_result = clean_llm_text(result)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url or "https://youtube.com")],
        [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url or "https://example.com")]
    ])
    await send_long_message(message, cleaned_result, reply_markup=inline_keyboard)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Նոր պատահական սերիալ")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
        ],
        resize_keyboard=True
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը։", reply_markup=reply_keyboard)



@router.message(F.text.in_({"📘 Սերիալի նկարագրություն", "🔁 Նոր սերիալի նկարագրություն"}))
async def ask_description(message: Message, state: FSMContext):
    await state.set_state(SeriesStates.waiting_for_description)
    await message.answer("✍️ Նկարագրիր ինչպիսի սերիալ ես ուզում։", reply_markup=ReplyKeyboardRemove())

@router.message(SeriesStates.waiting_for_description)
async def handle_description(message: Message, state: FSMContext):
    desc = message.text
    await message.answer("🔍 Փնտրում եմ համապատասխան սերիալը...")

    result = suggest_series_by_description_llm(desc)
    trailer_url, watch_url = extract_links_from_text(result)
    cleaned_result = clean_llm_text(result)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url or "https://youtube.com")],
        [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url or "https://example.com")]
    ])
    await send_long_message(message, cleaned_result, reply_markup=inline_keyboard)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Նոր սերիալի նկարագրություն")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
        ],
        resize_keyboard=True
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը։", reply_markup=reply_keyboard)
    await state.clear()



@router.message(F.text == "🔍 Ասա սերիալի անունը")
async def ask_series_name(message: Message, state: FSMContext):
    await state.set_state(SeriesStates.waiting_for_series_name)
    await message.answer("📺 Գրիր սերիալի անունը։", reply_markup=ReplyKeyboardRemove())

@router.message(SeriesStates.waiting_for_series_name)
async def handle_series_name(message: Message, state: FSMContext):
    series_name = message.text
    await message.answer("🔍 Փնտրում եմ սերիալի մասին ամբողջական տվյալներ...")

    result = get_series_details_by_name_llm(series_name)
    trailer_url, watch_url = extract_links_from_text(result)
    cleaned_result = clean_llm_text(result)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url or "https://youtube.com")],
        [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url or "https://example.com")]
    ])
    await send_long_message(message, cleaned_result, reply_markup=inline_keyboard)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Նոր սերիալի անուն")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
        ],
        resize_keyboard=True
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը։", reply_markup=reply_keyboard)
    await state.clear()


@router.message(F.text == "🔍 Նոր սերիալի անուն")
async def repeat_series_name(message: Message, state: FSMContext):
    await ask_series_name(message, state)

def format_series_text(chunk: str) -> str:
    lines = chunk.strip().split("\n")
    data = {}

    for line in lines:
        if "Վերնագիր" in line:
            data["title"] = line.replace("🎥 Վերնագիր՝", "").strip()
        elif "Ժանրը" in line:
            data["genre"] = line.replace("🎭 Ժանրը՝", "").strip()
        elif "Ռեժիսոր" in line:
            data["director"] = line.replace("🎬 Ռեժիսոր՝", "").strip()
        elif "Դերասաններ" in line:
            data["actors"] = line.replace("🎭 Դերասաններ՝", "").strip()
        elif "Սյուժե" in line:
            data["plot"] = line.replace("📜 Սյուժե՝", "").strip()
        elif "IMDb գնահատական" in line:
            data["rating"] = line.replace("📊 IMDb գնահատական՝", "").strip()

    formatted = (
        f"<b>🎥 {data.get('title', '')}</b>\n"
        f"🎭 <b>Ժանրը՝</b> {data.get('genre', '')}\n"
        f"🎬 <b>Ռեժիսոր՝</b> {data.get('director', '')}\n"
        f"🧑‍🎤 <b>Դերասաններ՝</b> {data.get('actors', '')}\n"
        f"📜 <b>Սյուժե՝</b> {data.get('plot', '')}\n"
        f"📊 <b>IMDb գնահատական՝</b> {data.get('rating', '')}"
    )
    return formatted


async def send_series_blocks(text: str, message: Message):
    series_chunks = split_movies(text)  # ✅ OK այսպես պահել

    for chunk in series_chunks:
        trailer_url, watch_url = extract_links_from_text(chunk)
        pretty_text = format_series_text(chunk)

        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url)],
            [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url)]
        ])
        await message.answer(pretty_text, parse_mode="HTML", reply_markup=inline_keyboard)



@router.message(F.text == "🔥 Լավագույն 10 սերիալ")
async def top_10_series_handler(message: Message):
    await message.answer("📺 Ընտրում եմ լավագույն սերիալները...")

    result = get_top_10_series_llm()
    await send_series_blocks(result, message)

    await message.answer("⬇️ Ընտրիր հաջորդ քայլը։", reply_markup=series_menu)


@router.message(F.text == "🎭 Սերիալ ըստ ժանրի")
async def ask_series_genre(message: Message, state: FSMContext):
    await message.answer("📺 Ընտրիր սերիալի ժանրը։", reply_markup=series_genre_menu)
    await state.set_state(SeriesStates.waiting_for_genre)


@router.message(SeriesStates.waiting_for_genre)
async def handle_series_genre(message: Message, state: FSMContext):
    selected = message.text.strip()
    genre = SERIES_GENRE_MAP.get(selected)

    if not genre:
        await message.answer("❌ Չճանաչված ժանր։ Խնդրում եմ ընտրիր ցանկից։", reply_markup=series_genre_menu)
        return

    await message.answer(f"🔍 Փնտրում եմ `{selected}` ժանրով սերիալներ...")

    result = get_series_by_genre_llm(genre)
    await send_series_blocks(result, message)

    await message.answer("🤖 Կարող ես ընտրել այլ ժանր կամ վերադառնալ մենյու։", reply_markup=series_genre_menu)
    await state.set_state(SeriesStates.waiting_for_genre)