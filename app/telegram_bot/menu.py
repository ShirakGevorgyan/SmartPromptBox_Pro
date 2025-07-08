from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🎛️ Գլխավոր մենյու
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 Mood Assistant")],
        [KeyboardButton(text="🎬 Ֆիլմեր և Սերիալներ"), KeyboardButton(text="🎵 Երգեր")],
        [KeyboardButton(text="📜 Հիշողություն"), KeyboardButton(text="🎼 Իմ Playlist-ը")],
        [KeyboardButton(text="🎙 Ձայնային հարցում"), KeyboardButton(text="🌍 GPT խոսակցություն")],
        [KeyboardButton(text="🎨 Նկար գեներացիա")],
        [KeyboardButton(text="📖 Պատմության շարունակություն"), KeyboardButton(text="✍️ Բանաստեղծություն / Քառյակ")],
        [KeyboardButton(text="📅 Օրվա առաջարկ")]
    ],
    resize_keyboard=True
)

# 🧠 Mood Assistant տրամադրության ընտրության մենյու
mood_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="😢 Տխուր եմ"), KeyboardButton(text="🥰 Սիրահարված եմ")],
        [KeyboardButton(text="😤 Զայրացած եմ"), KeyboardButton(text="😐 Ուղղակի լավ եմ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

# 🧠 Mood Assistant ենթաբաժիններ տրամադրության հիման վրա
mood_options_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎵 5 երգ"), KeyboardButton(text="🎬 5 ֆիլմ")],
        [KeyboardButton(text="💬 5 մեջբերում"), KeyboardButton(text="🖼 2 նկարների նկարագրություն")],
        [KeyboardButton(text="🔙 Վերադառնալ տրամադրության ընտրությանը")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

# 🎬 Ֆիլմեր ենթամենյու
movie_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎭 Ժանրով առաջարկներ")],
        [KeyboardButton(text="🔥 Լավագույն 10 ֆիլմ"), KeyboardButton(text="📺 Լավագույն սերիալներ")],
        [KeyboardButton(text="🧠 Խորը իմաստով ֆիլմեր")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

# 🎵 Երգեր ենթամենյու
# song_menu = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="🔤 Ստացիր բառերը"), KeyboardButton(text="⬇️ Ներբեռնել երգը")],
#         [KeyboardButton(text="❤️ Տրամադրությամբ երգեր"), KeyboardButton(text="🎧 Սիրած երգեր")],
#         [KeyboardButton(text="🔀 Պատահական երգ"), KeyboardButton(text="🎵 Ուղարկված երգեր")],  # Ավելացված կոճակ
#         [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
#     ],
#     resize_keyboard=True

song_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔤 Ստացիր բառերը"), KeyboardButton(text="⬇️ Ներբեռնել երգը")],
        [KeyboardButton(text="❤️ Տրամադրությամբ երգեր"), KeyboardButton(text="🎧 Սիրած երգեր")],
        [KeyboardButton(text="🔀 Պատահական երգ"), KeyboardButton(text="🎵 Ուղարկված երգեր")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)


# 📜 Հիշողություն ենթամենյու
memory_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🕘 Նախորդ հարցումներ")],
        [KeyboardButton(text="⭐ Ֆավորիտներ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

# 🎼 Playlist ենթամենյու
playlist_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎼 GPT Playlist առաջարկ"), KeyboardButton(text="🧠 Ըստ տրամադրության")],
        [KeyboardButton(text="📝 Իմ կազմած Playlist-ները")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

# 📖 Պատմության ենթամենյու
story_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✍️ Շարունակիր պատմությունը")],
        [KeyboardButton(text="📚 Ստեղծիր նոր պատմություն")],
        [KeyboardButton(text="📖 Իմ պատմությունները")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

# ✍️ Բանաստեղծություն ենթամենյու
poetry_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💌 Սիրային քառյակ"), KeyboardButton(text="🔥 Rap տողեր")],
        [KeyboardButton(text="🎭 Փիլիսոփայական տողեր")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)
