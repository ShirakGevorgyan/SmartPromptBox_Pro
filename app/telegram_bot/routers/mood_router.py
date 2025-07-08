from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.telegram_bot.menu import mood_menu, mood_options_menu, main_menu

from app.llm.mood_inferencer import (
    generate_songs_for_mood,
    generate_movies_for_mood,
    generate_quotes_for_mood,
)
from app.llm.image_generator import (
    generate_image_prompts_from_mood,
    generate_images_from_prompts,
)

router = Router()

# ✅ Mood state պահելու համար FSM
@router.message(F.text == "🧠 Mood Assistant")
async def mood_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ընտրիր քո տրամադրությունը 👇", reply_markup=mood_menu)

# ✅ Օգտատիրոջ տրամադրությունը պահել
@router.message(F.text.in_([
    "😢 Տխուր եմ", "🥰 Սիրահարված եմ",
    "😤 Զայրացած եմ", "😐 Ուղղակի լավ եմ"
]))
async def mood_chosen(message: Message, state: FSMContext):
    mood = message.text
    await state.update_data(mood=mood)
    await message.answer("Ի՞նչ ես ուզում ստանալ այդ տրամադրությամբ 😇", reply_markup=mood_options_menu)

# ✅ Ըստ mood-ի՝ տարբեր բաժինների գեներացիա
@router.message(F.text.in_([
    "🎵 5 երգ", "🎬 5 ֆիլմ", "💬 5 մեջբերում", "🖼 2 նկարների նկարագրություն"
]))
async def mood_generate(message: Message, state: FSMContext):
    user_data = await state.get_data()
    mood = user_data.get("mood", "😐 Ուղղակի լավ եմ")

    await message.answer("Սպասիր մի պահ… 🤖 մշակվում է…")

    if message.text == "🎵 5 երգ":
        result = generate_songs_for_mood(mood)
        await message.answer(result)

    elif message.text == "🎬 5 ֆիլմ":
        result = generate_movies_for_mood(mood)
        await message.answer(result)

    elif message.text == "💬 5 մեջբերում":
        result = generate_quotes_for_mood(mood)
        await message.answer(result)

    elif message.text == "🖼 2 նկարների նկարագրություն":
        prompt_list = generate_image_prompts_from_mood(mood)
        images = generate_images_from_prompts(prompt_list)
        for i, (prompt, image_url) in enumerate(images, 1):
            if image_url.startswith("http"):
                await message.answer_photo(photo=image_url, caption=f"Նկար {i}՝\n{prompt}")
            else:
                await message.answer(f"❌ Սխալ՝ `{prompt}`\n{image_url}")

    else:
        await message.answer("❌ Չհաջողվեց հասկանալ հարցումը։")

    await message.answer("Ընտրիր այլ բովանդակություն կամ փոխիր տրամադրությունը։", reply_markup=mood_options_menu)

# ✅ Վերադառնալ տրամադրության ընտրությանը
@router.message(F.text == "🔙 Վերադառնալ տրամադրության ընտրությանը")
async def back_to_mood(message: Message):
    await message.answer("Ընտրիր նոր տրամադրություն 👇", reply_markup=mood_menu)

# ✅ Վերադառնալ գլխավոր մենյու
@router.message(F.text == "🔝 Վերադառնալ գլխավոր մենյու")
async def back_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Դու վերադարձար գլխավոր մենյու 🏠", reply_markup=main_menu)
