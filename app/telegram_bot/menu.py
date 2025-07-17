from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🎛️ Գլխավոր մենյու
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 Mood Assistant")],
        [KeyboardButton(text="🎬 Ֆիլմեր և Սերիալներ"), KeyboardButton(text="🎵 Երգեր")],
        # [KeyboardButton(text="📜 Հիշողություն"), KeyboardButton(text="🎼 Իմ Playlist-ը")],
        [KeyboardButton(text="⭐️ Խոսիր ինձ հետ"),KeyboardButton(text="🎨 Նկար գեներացիա")],
        # [KeyboardButton(text="📅 Օրվա առաջարկ")]
    ],
    resize_keyboard=True
)

# 🧠 Mood Assistant տրամադրության ընտրության մենյու
mood_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="😢 Տխուր եմ"), KeyboardButton(text="🥰 Սիրահարված եմ")],
        [KeyboardButton(text="😤 Զայրացած եմ"), KeyboardButton(text="😐 Ուղղակի լավ եմ")],
        [KeyboardButton(text="🤩 Ուրախ եմ"), KeyboardButton(text="😴 Հոգնած եմ")],
        [KeyboardButton(text="🤯 Սթրեսային վիճակում եմ"), KeyboardButton(text="😎 Մոտիվացված եմ")],
        [KeyboardButton(text="😔 Մենակ եմ"), KeyboardButton(text="💭 Խորհում եմ")],
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


song_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬇️ Ներբեռնել երգ"), KeyboardButton(text="❤️ Տրամադրությամբ երգեր")],
        [KeyboardButton(text="🔀 Պատահական երգ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

random_song_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔁 Նոր պատահական երգ")],
        [KeyboardButton(text="🏠 Գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

song_action_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎵 Նոր երգ")],
        [KeyboardButton(text="🔙 Տրամադրության մենյու"), KeyboardButton(text="🏠 Գլխավոր մենյու")]
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

gpt_reply_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
        [KeyboardButton(text="🧹 Մաքրել զրույցը")]
    ],
    resize_keyboard=True
)


movie_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎞 Ֆիլմի նկարագրություն")],
        [KeyboardButton(text="🎲 Պատահական ֆիլմ")],
        # [KeyboardButton(text="😊 Ֆիլմ ըստ տրամադրության")],
        [KeyboardButton(text="🔍 Ասա ֆիլմի անունը")],
        [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)



series_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📘 Սերիալի նկարագրություն")],
        [KeyboardButton(text="🎲 Պատահական սերիալ")],
        # [KeyboardButton(text="😊 Սերիալ ըստ տրամադրության")],
        [KeyboardButton(text="🔍 Ասա սերիալի անունը")],
        [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

film_and_series_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎥 Ֆիլմեր")],
        [KeyboardButton(text="📺 Սերիալներ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ],
    resize_keyboard=True
)

img_menu = ReplyKeyboardMarkup(
    keyboard=[
        # [KeyboardButton(text="🔁 Նոր նկար գեներացնել")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]
    ]
)
