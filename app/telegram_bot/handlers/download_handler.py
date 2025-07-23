# from aiogram import Router, F
# from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, FSInputFile
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# import asyncio
# import os
# from app.utils.youtube_downloader import download_audio, download_video
# from app.llm.clean_title import clean_song_title_llm

# router = Router()

# class DownloadStates(StatesGroup):
#     waiting_for_url = State()
#     choosing_format = State()
#     choosing_quality = State()

# @router.message(F.text == "⬇️ Ներբեռնել երգ")
# async def start_download(message: Message, state: FSMContext):
#     await message.answer("📎 Ուղարկիր YouTube հղումը:")
#     await state.set_state(DownloadStates.waiting_for_url)

# @router.message(DownloadStates.waiting_for_url)
# async def receive_url(message: Message, state: FSMContext):
#     await state.update_data(url=message.text)

#     format_keyboard = ReplyKeyboardMarkup(
#         keyboard=[[KeyboardButton(text="🎵 Աուդիո"), KeyboardButton(text="🎥 Վիդեո")]],
#         resize_keyboard=True
#     )
#     await message.answer("📥 Որ տարբերակով ես ուզում ներբեռնել?", reply_markup=format_keyboard)
#     await state.set_state(DownloadStates.choosing_format)

# @router.message(DownloadStates.choosing_format)
# async def choose_format(message: Message, state: FSMContext):
#     user_choice = message.text
#     await state.update_data(format=user_choice)

#     if user_choice == "🎥 Վիդեո":
#         quality_keyboard = ReplyKeyboardMarkup(
#             keyboard=[
#                 [KeyboardButton(text="🔺 720p"), KeyboardButton(text="🔹 480p")],
#                 [KeyboardButton(text="🔸 360p"), KeyboardButton(text="🔻 240p")]
#             ],
#             resize_keyboard=True
#         )
#         await message.answer("📺 Ընտրիր որակը:", reply_markup=quality_keyboard)
#         await state.set_state(DownloadStates.choosing_quality)
#     else:
#         data = await state.get_data()
#         url = data["url"]
#         await message.answer("⏳ Ներբեռնում եմ աուդիոն․․․", reply_markup=ReplyKeyboardRemove())

#         # Մաքրել վերնագիրը LLM-ով
#         from yt_dlp import YoutubeDL
#         with YoutubeDL({'quiet': True}) as ydl:
#             info = ydl.extract_info(url, download=False)
#         raw_title = f"{info.get('uploader', 'Unknown')} - {info.get('title', 'Untitled')}"
#         clean_title = clean_song_title_llm(raw_title)

#         file_path = await asyncio.to_thread(download_audio, url, clean_title)

#         if not os.path.exists(file_path):
#             await message.answer("❌ Աուդիոն ներբեռնել չհաջողվեց։")
#             await state.clear()
#             return

#         clean_name = os.path.splitext(os.path.basename(file_path))[0]
#         document = FSInputFile(path=file_path, filename=f"{clean_name}.mp3")
#         await message.answer_document(document, caption=clean_name)
#         os.remove(file_path)

#         await message.answer(
#             "✅ Ներբեռնումը ավարտված է։\nՍեղմիր «🔁 Նոր հղում ուղարկել» և ուղարկիր նոր հղում:",
#             reply_markup=ReplyKeyboardMarkup(
#                 keyboard=[[KeyboardButton(text="🔁 Նոր հղում ուղարկել")],
#                             [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]],
#                 resize_keyboard=True,
#                 one_time_keyboard=True
#             )
#         )
#         await state.clear()

# @router.message(DownloadStates.choosing_quality)
# async def choose_quality(message: Message, state: FSMContext):
#     data = await state.get_data()
#     url = data["url"]
#     quality = message.text.replace("🔺", "").replace("🔹", "").replace("🔸", "").replace("🔻", "").strip()

#     await message.answer(f"⏳ Ներբեռնում եմ վիդեոն՝ {quality} որակով․․․", reply_markup=ReplyKeyboardRemove())

#     # Մաքրել վերնագիրը LLM-ով
#     from yt_dlp import YoutubeDL
#     with YoutubeDL({'quiet': True}) as ydl:
#         info = ydl.extract_info(url, download=False)
#     raw_title = f"{info.get('uploader', 'Unknown')} - {info.get('title', 'Untitled')}"
#     clean_title = clean_song_title_llm(raw_title)

#     file_path = await asyncio.to_thread(download_video, url, quality, clean_title)

#     if not os.path.exists(file_path):
#         await message.answer("❌ Վիդեոն ներբեռնել չհաջողվեց։")
#         await state.clear()
#         return

#     clean_name = os.path.splitext(os.path.basename(file_path))[0]
#     video_file = FSInputFile(path=file_path, filename=f"{clean_name}.mp4")
#     await message.answer_video(video_file, caption=clean_name)
#     os.remove(file_path)

#     await message.answer(
#         "✅ Ներբեռնումը ավարտված է։\nՈւզում ես նոր հղում ուղարկել? Սեղմիր «🔁 Նոր հղում ուղարկել»:",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=[[KeyboardButton(text="🔁 Նոր հղում ուղարկել")],
#                         [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]],
#             resize_keyboard=True,
#             one_time_keyboard=True
#         )
#     )
#     await state.clear()

# @router.message(F.text == "🔁 Նոր հղում ուղարկել")
# async def restart_download(message: Message, state: FSMContext):
#     await message.answer("📎 Ուղարկիր YouTube հղումը:")
#     await state.set_state(DownloadStates.waiting_for_url)
