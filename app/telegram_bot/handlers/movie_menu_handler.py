from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

from app.telegram_bot.menu import (
    movie_menu,
    film_and_series_menu,
    main_menu,
)
from app.llm.movie_picker import (
    get_random_movie_llm,
    suggest_movies_by_description_llm,
    get_movie_details_by_name_llm
)

router = Router()

# --- States ---
class FilmStates(StatesGroup):
    waiting_for_description = State()
    waiting_for_movie_name = State()


# --- ՕԳՆԱԿԱՆ ՖՈՒՆԿՑԻԱՆԵՐ ---
def extract_links_from_text(text: str):
    trailer_match = re.search(r"▶️ Տրեյլեր՝ \[.*?\]\((.*?)\)", text)
    watch_match = re.search(r"🎞️ Դիտելու հղում՝ \[.*?\]\((.*?)\)", text)
    return (
        trailer_match.group(1) if trailer_match else "https://youtube.com",
        watch_match.group(1) if watch_match else "https://www.imdb.com"
    )

def clean_llm_text(text: str) -> str:
    lines = text.strip().split("\n")
    cleaned_lines = [line for line in lines if not line.startswith("▶️") and not line.startswith("🎞️")]
    return "\n".join(cleaned_lines)


# --- ՄԵՆՅՈՒՆԵՐ ---
@router.message(F.text.func(lambda text: text.strip() == "🎬 Ֆիլմեր և Սերիալներ"))
async def open_film_and_series_menu(message: Message):
    await message.answer("🎥 Ընտրիր՝ ֆիլմեր թե սերիալներ։", reply_markup=film_and_series_menu)

@router.message(F.text == "🎥 Ֆիլմեր")
async def show_film_menu(message: Message):
    await message.answer("🎥 Ընտրիր գործողությունը ֆիլմերի համար։", reply_markup=movie_menu)

@router.message(F.text == "🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")
async def back_to_film_series_menu(message: Message):
    await message.answer("📚 Վերադարձիր Ֆիլմերի և Սերիալների ընտրությանը։", reply_markup=film_and_series_menu)

@router.message(F.text == "🔝 Վերադառնալ գլխավոր մենյու")
async def back_to_main_menu(message: Message):
    await message.answer("🏠 Գլխավոր մենյու", reply_markup=main_menu)


# --- Պատահական ֆիլմ ---
@router.message(F.text.in_({"🎲 Պատահական ֆիլմ", "🔁 Նոր պատահական ֆիլմ"}))
async def send_random_movie(message: Message):
    await message.answer("🎯 Ընտրում եմ պատահական ֆիլմ... ⏳")
    result = get_random_movie_llm()
    trailer_url, watch_url = extract_links_from_text(result)
    cleaned_result = clean_llm_text(result)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url)],
        [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url)]
    ])
    await message.answer(cleaned_result, reply_markup=inline_keyboard)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Նոր պատահական ֆիլմ")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
        ],
        resize_keyboard=True
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը։", reply_markup=reply_keyboard)


# --- Ֆիլմի նկարագրությամբ որոնում ---
@router.message(F.text.in_({"🎞 Ֆիլմի նկարագրություն", "🔁 Նոր Ֆիլմի նկարագրություն"}))
async def ask_description(message: Message, state: FSMContext):
    await state.set_state(FilmStates.waiting_for_description)
    await message.answer("✍️ Նկարագրիր ինչպիսի ֆիլմ ես ուզում։", reply_markup=ReplyKeyboardRemove())

@router.message(FilmStates.waiting_for_description)
async def handle_description(message: Message, state: FSMContext):
    desc = message.text
    await message.answer("🔍 Փնտրում եմ համապատասխան ֆիլմը...")

    result = suggest_movies_by_description_llm(desc)
    trailer_url, watch_url = extract_links_from_text(result)
    cleaned_result = clean_llm_text(result)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url)],
        [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url)]
    ])
    await message.answer(cleaned_result, reply_markup=inline_keyboard)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Նոր Ֆիլմի նկարագրություն")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
        ],
        resize_keyboard=True
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը։", reply_markup=reply_keyboard)
    await state.clear()


# --- Ֆիլմի անունով որոնում ---
@router.message(F.text == "🔍 Ասա ֆիլմի անունը")
async def ask_movie_name(message: Message, state: FSMContext):
    await state.set_state(FilmStates.waiting_for_movie_name)
    await message.answer("🎬 Գրիր ֆիլմի անունը։", reply_markup=ReplyKeyboardRemove())

@router.message(FilmStates.waiting_for_movie_name)
async def handle_movie_name(message: Message, state: FSMContext):
    movie_name = message.text
    await message.answer("🔍 Փնտրում եմ ֆիլմի մասին ամբողջական տվյալներ...")

    result = get_movie_details_by_name_llm(movie_name)
    trailer_url, watch_url = extract_links_from_text(result)
    cleaned_result = clean_llm_text(result)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎞 Տրեյլեր", url=trailer_url)],
        [InlineKeyboardButton(text="🌐 Դիտել", url=watch_url)]
    ])
    await message.answer(cleaned_result, reply_markup=inline_keyboard)

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Նոր ֆիլմի անուն")],
            [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
            [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
        ],
        resize_keyboard=True
    )
    await message.answer("⬇️ Ընտրիր հաջորդ քայլը։", reply_markup=reply_keyboard)
    await state.clear()

@router.message(F.text == "🔍 Նոր ֆիլմի անուն")
async def repeat_movie_name(message: Message, state: FSMContext):
    await ask_movie_name(message, state)
