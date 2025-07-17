from aiogram import F, Router
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os

from app.telegram_bot.menu import main_menu, img_menu  # ավելացրել ենք main_menu
from app.llm.img_generator import generate_image

router = Router()

class ImageStates(StatesGroup):
    waiting_for_prompt = State()

@router.message(F.text == "🎨 Նկար գեներացիա")
@router.message(F.text == "🔁 Նոր նկարագրություն ուղարկել")
async def ask_for_prompt(message: Message, state: FSMContext):
    await message.answer(
        "✏️ Տուր նկարագրություն նկար գեներացնելու համար 🖼️",
        reply_markup=img_menu
    )
    await state.set_state(ImageStates.waiting_for_prompt)

@router.message(ImageStates.waiting_for_prompt)
async def handle_prompt(message: Message, state: FSMContext):
    prompt = message.text
    await message.answer("🎨 Ստեղծում եմ նկարը, մի պահ սպասիր...")

    try:
        image_path = generate_image(prompt)

        if not image_path or not os.path.exists(image_path):
            await message.answer(
                "❌ Սխալ՝ նկարը չստացվեց։",
                reply_markup=img_menu
            )
        else:
            file = FSInputFile(image_path)
            await message.answer_photo(
                photo=file,
                caption="✅ Ահա քո նկարը"
            )
            os.remove(image_path)

            # Նոր ընտրացանկ գեներացումից հետո
            await message.answer(
                "🔚 Ինչ ես ուզում անել հաջորդը?",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="🔁 Նոր նկարագրություն ուղարկել")],
                        [KeyboardButton(text="🏠 Վերադառնալ գլխավոր մենյու")],
                    ],
                    resize_keyboard=True,
                    one_time_keyboard=False
                )
            )

    except Exception as e:
        await message.answer(
            f"❌ Սխալ՝ {str(e)}",
            reply_markup=img_menu
        )

    await state.clear()

@router.message(F.text == "🏠 Վերադառնալ գլխավոր մենյու")
async def go_to_main_menu(message: Message, state: FSMContext):
    await message.answer("🏠 Վերադարձանք գլխավոր մենյու 📋", reply_markup=main_menu)
    await state.clear()
