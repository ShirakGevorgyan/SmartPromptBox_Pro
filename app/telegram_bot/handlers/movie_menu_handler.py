"""Movie menu handlers.

Provides Telegram flows to:
- open the parent "Films & Series" menu and the movie submenu,
- suggest a random movie via LLM,
- get a movie by free-text description,
- get a movie by exact name,
- list movies by genre,
- list top-10 movies.

Also includes tiny helpers for extracting trailer/watch links from the LLM
output and cleaning/segmenting the returned text.
"""

from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

from app.telegram_bot.menu import (
    movie_menu,
    film_and_series_menu,
    main_menu,
    movie_genre_menu,
)
from app.llm.movie_picker import (
    get_random_movie_llm,
    suggest_movies_by_description_llm,
    get_movie_details_by_name_llm,
    get_movies_by_genre_llm,
    get_top_10_movies_llm,
)

router = Router()


class FilmStates(StatesGroup):
    """FSM states used when the user is typing description/name/genre."""

    waiting_for_description = State()
    waiting_for_movie_name = State()
    waiting_for_genre = State()


GENRE_MAP = {
    "🎬 Ակցիա": "Action",
    "😂 Կատակերգություն": "Comedy",
    "😱 Սարսափ": "Horror",
    "🎭 Դրամա": "Drama",
    "💘 Ռոմանտիկա": "Romance",
    "🕵️ Թրիլեր": "Thriller",
    "🚀 Գիտաֆանտաստիկա": "Sci-Fi",
    "🧙 Ֆանտազիա": "Fantasy",
    "🎥 Պատմական": "Historical",
    "👨‍👩‍👧 Ընտանեկան": "Family",
}


def extract_links_from_text(text: str):
    """Extract trailer and watch URLs from an LLM-formatted block.

    The block is expected to contain lines:
        ▶️ Տրեյլեր՝ [..](URL)
        🎞️ Դիտելու հղում՝ [..](URL)

    Returns:
        tuple[str, str]: (trailer_url, watch_url) with safe fallbacks.
    """
    trailer_match = re.search(r"▶️ Տրեյլեր՝ \[.*?\]\((.*?)\)", text)
    watch_match = re.search(r"🎞️ Դիտելու հղում՝ \[.*?\]\((.*?)\)", text)
    return (
        trailer_match.group(1) if trailer_match else "https://youtube.com",
        watch_match.group(1) if watch_match else "https://www.imdb.com",
    )


def clean_llm_text(text: str) -> str:
    """Remove explicit trailer/watch lines (we show them as buttons instead)."""
    lines = text.strip().split("\n")
    cleaned_lines = [
        line for line in lines if not line.startswith("▶️") and not line.startswith("🎞️")
    ]
    return "\n".join(cleaned_lines)


@router.message(F.text.func(lambda text: text.strip() == "🎬 Ֆիլմեր և Սերիալներ"))
async def open_film_and_series_menu(message: Message):
    """Open the parent 'Films & Series' menu."""
    await message.answer(
        "🎥 Ընտրիր՝ ֆիլմեր թե սերիալներ։", reply_markup=film_and_series_menu
    )


@router.message(F.text == "🎥 Ֆիլմեր")
async def show_film_menu(message: Message):
    """Open the movie submenu."""
    await message.answer(
        "🎥 Ընտրիր գործողությունը ֆիլմերի համար։", reply_markup=movie_menu
    )


@router.message(F.text == "🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")
async def back_to_film_series_menu(message: Message):
    """Back to the parent menu."""
    await message.answer(
        "📚 Վերադարձիր Ֆիլմերի և Սերիալների ընտրությանը։",
        reply_markup=film_and_series_menu,
    )


@router.message(F.text == "🔝 Վերադառնալ գլխավոր մենյու")
async def back_to_main_menu(message: Message):
    """Back to the main menu."""
    await message.answer("🏠 Գլխավոր մենյու", reply_markup=main_menu)


@router.message(F.text.in_({"🎲 Պատահական ֆիլմ", "🔁 Նոր պատահական ֆիլմ"}))
async def send_random_movie(message: Message):
    """Ask LLM for a random movie, clean text, and attach link buttons."""
    await message.answer("🎯 Ընտրում եմ պատահական ֆիլմ... ⏳")
    result = get_random_movie_llm()
    trailer_url, watch_url = extract_links_from_text(result)
    cleaned_result = clean_llm_text(result)

    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url)],
            [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url)],
        ]
    )
    await message.answer(cleaned_result, reply_markup=inline_keyboard)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Նոր պատահական ֆիլմ")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
        ],
        resize_keyboard=True,
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը।", reply_markup=reply_keyboard)


@router.message(F.text.in_({"🎞 Ֆիլմի նկարագրություն", "🔁 Նոր Ֆիլմի նկարագրություն"}))
async def ask_description(message: Message, state: FSMContext):
    """Ask the user for a free-text description and enter the description state."""
    await state.set_state(FilmStates.waiting_for_description)
    await message.answer(
        "✍️ Նկարագրիր ինչպիսի ֆիլմ ես ուզում։", reply_markup=ReplyKeyboardRemove()
    )


@router.message(FilmStates.waiting_for_description)
async def handle_description(message: Message, state: FSMContext):
    """Fetch movie suggestion by description and show trailer/watch buttons."""
    desc = message.text
    await message.answer("🔍 Փնտրում եմ համապատասխան ֆիլմը...")

    result = suggest_movies_by_description_llm(desc)
    trailer_url, watch_url = extract_links_from_text(result)
    cleaned_result = clean_llm_text(result)

    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url)],
            [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url)],
        ]
    )
    await message.answer(cleaned_result, reply_markup=inline_keyboard)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Նոր Ֆիլմի նկարագրություն")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
        ],
        resize_keyboard=True,
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը।", reply_markup=reply_keyboard)
    await state.clear()


# --- Ֆիլմի անունով որոնում ---
@router.message(F.text == "🔍 Ասա ֆիլմի անունը")
async def ask_movie_name(message: Message, state: FSMContext):
    """Ask for a movie title and enter the corresponding state."""
    await state.set_state(FilmStates.waiting_for_movie_name)
    await message.answer("🎬 Գրիր ֆիլմի անունը։", reply_markup=ReplyKeyboardRemove())


@router.message(FilmStates.waiting_for_movie_name)
async def handle_movie_name(message: Message, state: FSMContext):
    """Fetch full details by movie name and display with link buttons."""
    movie_name = message.text
    await message.answer("🔍 Փնտրում եմ ֆիլմի մասին ամբողջական տվյալներ...")

    result = get_movie_details_by_name_llm(movie_name)
    trailer_url, watch_url = extract_links_from_text(result)
    cleaned_result = clean_llm_text(result)

    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url)],
            [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url)],
        ]
    )
    await message.answer(cleaned_result, reply_markup=inline_keyboard)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Նոր ֆիլմի անուն")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
        ],
        resize_keyboard=True,
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը।", reply_markup=reply_keyboard)
    await state.clear()


@router.message(F.text == "🔍 Նոր ֆիլմի անուն")
async def repeat_movie_name(message: Message, state: FSMContext):
    """Shortcut to repeat the 'ask movie name' flow."""
    await ask_movie_name(message, state)


def split_movies(text: str) -> list[str]:
    """Split a long LLM response into per-movie blocks.

    Assumes each movie starts with a line like:
        🎥 Վերնագիր` ...

    Returns:
        list[str]: non-empty, trimmed chunks.
    """
    chunks = re.split(r"(?=🎥 Վերնագիր)", text.strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


async def send_movie_blocks(text: str, message: Message):
    """Send each movie chunk as a separate message with link buttons."""
    movie_chunks = split_movies(text)

    for chunk in movie_chunks:
        trailer_url, watch_url = extract_links_from_text(chunk)
        cleaned = clean_llm_text(chunk)

        inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url)],
                [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url)],
            ]
        )
        await message.answer(cleaned, reply_markup=inline_keyboard)


@router.message(F.text == "🎭 Ժանրով առաջարկներ")
async def ask_movie_genre(message: Message, state: FSMContext):
    """Show the movie genre keyboard and enter the genre state."""
    await message.answer("🎭 Ընտրիր ֆիլմի ժանրը։", reply_markup=movie_genre_menu)
    await state.set_state(FilmStates.waiting_for_genre)


@router.message(FilmStates.waiting_for_genre)
async def handle_movie_genre(message: Message, state: FSMContext):
    """List movies for the chosen genre and keep the state for more selections."""
    user_input = message.text.strip()
    genre = GENRE_MAP.get(user_input)

    if not genre:
        await message.answer(
            "❌ Չճանաչված ժանր։ Խնդրում եմ ընտրիր ցանկից։",
            reply_markup=movie_genre_menu,
        )
        return

    await message.answer(f"🎬 Փնտրում եմ `{user_input}` ժանրով ֆիլմեր...")

    result = get_movies_by_genre_llm(genre)
    await send_movie_blocks(result, message)

    await message.answer(
        "🤖 Կրկին ընտրի այլ ժանր կամ վերադարձիր մենյու։", reply_markup=movie_genre_menu
    )
    await state.set_state(FilmStates.waiting_for_genre)


@router.message(F.text == "🔥 Լավագույն 10 ֆիլմ")
async def best_top_10_movies(message: Message):
    """Show a curated list of the top 10 movies using LLM suggestions."""
    await message.answer("🔥 Ընտրում եմ լավագույն 10 ֆիլմ...")

    result = get_top_10_movies_llm()
    await send_movie_blocks(result, message)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎭 Ժանրով առաջարկներ")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
        ],
        resize_keyboard=True,
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը।", reply_markup=reply_keyboard)
