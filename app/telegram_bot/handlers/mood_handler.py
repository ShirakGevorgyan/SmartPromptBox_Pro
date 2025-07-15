from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.telegram_bot.menu import mood_menu, mood_options_menu, main_menu
from app.llm.mood_inferencer import (
    generate_songs_for_mood,
    generate_movies_for_mood,
    generate_quotes_for_mood
)
from app.llm.image_generator import (
    generate_image_prompts_from_mood,
    generate_images_from_prompts,
)
from app.llm.clean_title import clean_song_title_llm
from app.utils.youtube_downloader import download_audio

router = Router()

# ✅ Mood Assistant մենյու
@router.message(F.text == "🧠 Mood Assistant")
async def mood_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ընտրիր քո տրամադրությունը 👇", reply_markup=mood_menu)

# ✅ Տրամադրության ընտրություն
@router.message(F.text.in_([
    "😢 Տխուր եմ", "🥰 Սիրահարված եմ",
    "😤 Զայրացած եմ", "😐 Ուղղակի լավ եմ",
    "🤩 Ուրախ եմ", "😴 Հոգնած եմ",
    "🤯 Սթրեսային վիճակում եմ", "😎 Մոտիվացված եմ",
    "😔 Մենակ եմ", "💭 Խորհում եմ"
]))
async def mood_chosen(message: Message, state: FSMContext):
    mood = message.text
    await state.update_data(mood=mood)
    await message.answer("Ի՞նչ ես ուզում ստանալ այդ տրամադրությամբ 😇", reply_markup=mood_options_menu)

# ✅ Ֆիլմեր ուղարկող ֆունկցիա
async def send_movies_as_buttons(movies: list[dict], message):
    for i, movie in enumerate(movies, 1):
        text = (
            f"<b>📽 Ֆիլմ {i}․ {movie['title']}</b>\n"
            f"🎭 <b>Ժանր</b>․ {movie['genre']}\n"
            f"🎬 <b>Ռեժիսոր</b>․ {movie['director']}"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎞 Տրեյլեր", url=movie['trailer_url'])],
            [InlineKeyboardButton(text="🌐 Դիտել", url=movie['watch_url'])]
        ])
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)

# ✅ Երգեր ուղարկող ֆունկցիա
async def send_song_buttons(songs: list[dict], message: Message, state: FSMContext):
    await state.update_data(songs_for_download=songs)  # store full list in FSM

    for idx, song in enumerate(songs):
        title = song["title"]
        artist = song["artist"]
        description = song["description"]
        youtube_url = song["youtube"]

        text = (
            f"<b>{title}</b> — <i>{artist}</i>\n"
            f"📎 {description}"
        )
        callback_data = f"download_{idx}"  # only index used here

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 YouTube", url=youtube_url)],
            [InlineKeyboardButton(text="⬇️ Ներբեռնել", callback_data=callback_data)]
        ])
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)

# ✅ Callback ֆունկցիա ներբեռնելու համար
@router.callback_query(F.data.startswith("download_"))
async def handle_download_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer("⬇️ Ներբեռնում եմ...")

    try:
        index = int(callback.data.split("_")[1])
        data = await state.get_data()
        songs = data.get("songs_for_download", [])

        if index < 0 or index >= len(songs):
            await callback.message.answer("❌ Սխալ ինդեքս։")
            return

        song = songs[index]
        youtube_url = song["youtube"]
        title = song["title"]

        clean_name = clean_song_title_llm(title)
        file_path = download_audio(youtube_url, filename=clean_name)
        audio = FSInputFile(file_path)

        await callback.message.answer_audio(audio, caption=f"🎵 {clean_name}")
        await callback.message.delete()

    except Exception as e:
        print("❌ Download error:", e)
        await callback.message.answer("Չհաջողվեց ներբեռնել երգը։")

# ✅ Mood-ի վրա հիմնված բովանդակություն
@router.message(F.text.in_([
    "🎵 5 երգ", "🎬 5 ֆիլմ", "💬 5 մեջբերում", "🖼 2 նկարների նկարագրություն"
]))
async def mood_generate(message: Message, state: FSMContext):
    user_data = await state.get_data()
    mood = user_data.get("mood", "😐 Ուղղակի լավ եմ")
    await message.answer("Սպասիր մի պահ… 🤖 մշակվում է…")

    if message.text == "🎵 5 երգ":
        song_data = generate_songs_for_mood(mood)
        if not song_data:
            await message.answer("Չհաջողվեց գեներացնել երգեր։ Փորձիր նորից 😢")
            return
        await message.answer("🎶 Գտնված 5 երգերը՝")
        await send_song_buttons(song_data, message, state)

    elif message.text == "🎬 5 ֆիլմ":
        movie_data = generate_movies_for_mood(mood)
        if not movie_data:
            await message.answer("Չհաջողվեց գտնել համապատասխան ֆիլմեր 😞 Փորձիր նորից  ")
            return
        await message.answer("🎥 Գտնված 5 ֆիլմերը՝")
        await send_movies_as_buttons(movie_data, message)

    elif message.text == "💬 5 մեջբերում":
        result = generate_quotes_for_mood(mood)
        await message.answer(result)

    elif message.text == "🖼 2 նկարների նկարագրություն":
        prompts = generate_image_prompts_from_mood(mood)
        images = generate_images_from_prompts(prompts)
        for i, (prompt, url) in enumerate(images, 1):
            if url.startswith("http"):
                await message.answer_photo(photo=url, caption=f"Նկար {i}՝\n{prompt}")
            else:
                await message.answer(f"❌ Սխալ՝ `{prompt}`\n{url}")
    else:
        await message.answer("❌ Չհաջողվեց հասկանալ հարցումը։")

    await message.answer("Ընտրիր այլ բովանդակություն կամ փոխիր տրամադրությունը։", reply_markup=mood_options_menu)
    
@router.message(F.text == "❤️ Տրամադրությամբ երգեր")
async def show_mood_menu(message: Message, state: FSMContext):
    # ջնջենք նախորդ տրամադրությունը (եթե կար)
    await state.clear()
    
    # ուղարկենք տրամադրությունների ընտրացանկը
    await message.answer(
        "🔍 Ընտրիր քո տրամադրությունը՝ ես կօգնեմ քեզ երգով 🎶",
        reply_markup=mood_menu
    ) 
    
# ✅ Վերադառնալ տրամադրության ընտրությանը
@router.message(F.text == "🔙 Վերադառնալ տրամադրության ընտրությանը")
async def back_to_mood(message: Message):
    await message.answer("Ընտրիր նոր տրամադրություն 👇", reply_markup=mood_menu)

# ✅ Վերադառնալ գլխավոր մենյու
@router.message(F.text == "🔝 Վերադառնալ գլխավոր մենյու")
async def back_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Դու վերադարձար գլխավոր մենյու 🏠", reply_markup=main_menu)
    

