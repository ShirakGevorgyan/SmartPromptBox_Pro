# from aiogram import Router, F
# from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile, ReplyKeyboardRemove
# from aiogram.fsm.context import FSMContext
# from app.states.voice_creation_states import VoiceCreationStates
# from app.telegram_bot.menu import main_menu
# from app.llm.bark_generator import bark_generate

# router = Router()

# # 🎤 Սկսել ձայնային երգի ստեղծումը
# @router.message(F.text == "🎤 Ստեղծել ձայնային երգ")
# async def start_voice_creation(message: Message, state: FSMContext):
#     # Սկսում ենք՝ սպասելով բառերին
#     await state.set_state(VoiceCreationStates.waiting_for_lyrics)
#     await message.answer("📄 Խնդրում եմ ուղարկիր քո երգի բառերը։")

# # ➕ Բառերը ստանալուց հետո
# @router.message(VoiceCreationStates.waiting_for_lyrics)
# async def get_lyrics(message: Message, state: FSMContext):
#     await state.update_data(lyrics=message.text)

#     # Սեռի ընտրության ստեղնաշար
#     gender_kb = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="🧑 Տղա"), KeyboardButton(text="👧 Աղջիկ")]
#         ],
#         resize_keyboard=True
#     )

#     await state.set_state(VoiceCreationStates.waiting_for_gender)
#     await message.answer("🎙 Ուզում ես տղայի՞, թե՞ աղջկա ձայնով հնչի։", reply_markup=gender_kb)

# # ➕ Սեռի ընտրությունից հետո
# @router.message(VoiceCreationStates.waiting_for_gender)
# async def get_gender(message: Message, state: FSMContext):
#     gender = message.text.strip().lower()
    
#     # Սեռը ֆիքսում ենք
#     if "տղա" in gender:
#         await state.update_data(voice="male")
#     elif "աղջիկ" in gender:
#         await state.update_data(voice="female")
#     else:
#         await message.answer("❗ Խնդրում եմ ընտրիր՝ 🧑 Տղա կամ 👧 Աղջիկ։")
#         return

#     # Ոճի ընտրության ստեղնաշար
#     style_kb = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="🎵 Ռեփ"), KeyboardButton(text="🎸 Ռոք")],
#             [KeyboardButton(text="🎤 Պոպ"), KeyboardButton(text="💘 Ռոմանտիկ"), KeyboardButton(text="❄️ Սառը")]
#         ],
#         resize_keyboard=True
#     )

#     await state.set_state(VoiceCreationStates.waiting_for_style)
#     await message.answer("🎼 Ի՞նչ ոճով երգ լինի։", reply_markup=style_kb)

# # ➕ Ոճի ընտրությունից հետո՝ ստեղծում ենք երգը
# @router.message(VoiceCreationStates.waiting_for_style)
# async def get_style_and_generate(message: Message, state: FSMContext):
#     data = await state.get_data()
#     lyrics = data.get("lyrics")
#     voice = data.get("voice")
#     style = message.text.strip().lower()

#     await message.answer("🎧 Ստեղծում եմ քո երգը... Խնդրում եմ սպասիր...")

#     try:
#         # Փորձում ենք գեներացնել ձայնային ֆայլը
#         audio_path = await bark_generate(lyrics, voice=voice, style=style)
#         audio_file = FSInputFile(audio_path)

#         # Ուղարկում ենք ձայնը
#         await message.answer_audio(audio_file, caption="✅ Քո երգը պատրաստ է։ 🎵")

#         # Հին ստեղնաշարը մաքրում ենք
#         await message.answer("🧹 Մաքրում եմ նախորդ ընտրությունները։", reply_markup=ReplyKeyboardRemove())

#         # Վերադարձ մենյու
#         await message.answer("🔙 Վերադառնալ գլխավոր մենյու։", reply_markup=main_menu)
#         await state.clear()

#     except Exception as e:
#         print("Bark Error:", e)
#         await message.answer("❌ Երգի ստեղծումը ձախողվեց։ Խնդրում եմ փորձիր նորից։")
