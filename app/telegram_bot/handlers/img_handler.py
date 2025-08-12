"""Handlers for the image generation feature.

Flow:
- ask_for_prompt: asks the user for a text prompt and sets FSM state.
- handle_prompt: calls the image generator, sends the photo, and offers next actions.
- go_to_main_menu: returns to the main menu (and clears the state).
"""

from aiogram import F, Router
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os

from app.telegram_bot.menu import main_menu, img_menu
from app.llm.img_generator import generate_image

router = Router()


class ImageStates(StatesGroup):
    """FSM states for image generation."""

    waiting_for_prompt = State()


@router.message(F.text == "🎨 Նկար գեներացիա")
@router.message(F.text == "🔁 Նոր նկարագրություն ուղարկել")
async def ask_for_prompt(message: Message, state: FSMContext):
    """Prompt the user to provide a text description for image generation."""
    await message.answer(
        "✏️ Տուր նկարագրություն նկար գեներացնելու համար 🖼️", reply_markup=img_menu
    )
    await state.set_state(ImageStates.waiting_for_prompt)


@router.message(ImageStates.waiting_for_prompt)
async def handle_prompt(message: Message, state: FSMContext):
    """Generate an image from the provided prompt and send it back to the user."""
    prompt = message.text
    await message.answer("🎨 Ստեղծում եմ նկարը, մի պահ սպասիր...")

    try:
        image_path = generate_image(prompt)

        if not image_path or not os.path.exists(image_path):
            await message.answer("❌ Սխալ՝ նկարը չստացվեց।", reply_markup=img_menu)
        else:
            file = FSInputFile(image_path)
            await message.answer_photo(photo=file, caption="✅ Ահա քո նկարը")
            os.remove(image_path)

            await message.answer(
                "🔚 Ինչ ես ուզում անել հաջորդը?",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="🔁 Նոր նկարագրություն ուղարկել")],
                        [KeyboardButton(text="🏠 Վերադառնալ գլխավոր մենյու")],
                    ],
                    resize_keyboard=True,
                    one_time_keyboard=False,
                ),
            )

    except Exception as e:
        await message.answer(f"❌ Սխալ՝ {str(e)}", reply_markup=img_menu)

    await state.clear()


@router.message(F.text == "🏠 Վերադառնալ գլխավոր մենյու")
async def go_to_main_menu(message: Message, state: FSMContext):
    """Return to the main menu and clear the FSM state."""
    await message.answer("🏠 Վերադարձանք գլխավոր մենյու 📋", reply_markup=main_menu)
    await state.clear()
