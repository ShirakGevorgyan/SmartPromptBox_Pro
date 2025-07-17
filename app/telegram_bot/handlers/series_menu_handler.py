from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

from app.telegram_bot.menu import (
    series_menu,
    film_and_series_menu,
    main_menu,
)
from app.llm.series_picker import (
    get_random_series_llm,
    suggest_series_by_description_llm,
    get_series_details_by_name_llm
)

router = Router()


# --- STATES ---
class SeriesStates(StatesGroup):
    waiting_for_description = State()
    waiting_for_series_name = State()


# --- ՕԳՆԱԿԱՆ ՖՈՒՆԿՑԻԱՆԵՐ ---
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


# --- ՄԵՆՅՈՒՆԵՐ ---
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


# --- ՊԱՏԱՀԱԿԱՆ ՍԵՐԻԱԼ ---
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


# --- ՆԿԱՐԱԳՐՈՒԹՅԱՄԲ ՍԵՐԻԱԼ ---
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


# --- ՍԵՐԻԱԼԻ ԱՆՈՒՆՈՎ ՓՆՏՐՈՒՄ ---
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
