from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 Mood Assistant")],
        [KeyboardButton(text="🎬 Ֆիլմեր և Սերիալներ"), KeyboardButton(text="🎵 Երգեր")],
        [
            KeyboardButton(text="🎨 Նկար գեներացիա"),
            KeyboardButton(text="⭐️ Խոսիր ինձ հետ"),
        ],
    ],
    resize_keyboard=True,
)

mood_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="😢 Տխուր եմ"), KeyboardButton(text="🥰 Սիրահարված եմ")],
        [
            KeyboardButton(text="😤 Զայրացած եմ"),
            KeyboardButton(text="😐 Ուղղակի լավ եմ"),
        ],
        [KeyboardButton(text="🤩 Ուրախ եմ"), KeyboardButton(text="😴 Հոգնած եմ")],
        [
            KeyboardButton(text="🤯 Սթրեսային վիճակում եմ"),
            KeyboardButton(text="😎 Մոտիվացված եմ"),
        ],
        [KeyboardButton(text="😔 Մենակ եմ"), KeyboardButton(text="💭 Խորհում եմ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)


mood_options_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎵 5 երգ"), KeyboardButton(text="🎬 5 ֆիլմ")],
        [
            KeyboardButton(text="💬 5 մեջբերում"),
            KeyboardButton(text="🖼 2 նկարների նկարագրություն"),
        ],
        [KeyboardButton(text="🔙 Վերադառնալ տրամադրության ընտրությանը")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)


song_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❤️ Տրամադրությամբ երգեր")],
        [
            KeyboardButton(text="🎧 Ըստ ոճի"),
            KeyboardButton(text="📝 Ըստ նկարագրության"),
        ],
        [KeyboardButton(text="🧑‍🎤 Արտիստի լավագույն երգերը")],
        [KeyboardButton(text="🔀 Պատահական երգ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)


genre_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎸 Ռոք"), KeyboardButton(text="🎹 Ջազ")],
        [KeyboardButton(text="🎤 Ռեփ"), KeyboardButton(text="🎶 Փոփ")],
        [KeyboardButton(text="💃 Լատինո"), KeyboardButton(text="🎻 Կլասիկ")],
        [KeyboardButton(text="🏞 Ֆոլք"), KeyboardButton(text="🎼 Էլեկտրոնային")],
        [KeyboardButton(text="🔥 Մետալ"), KeyboardButton(text="🎷 Ֆանկ")],
        [KeyboardButton(text="🔙 Վերադառնալ Երգեր մենյու")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)


random_song_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔁 Նոր պատահական երգ")],
        [KeyboardButton(text="🏠 Գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)

song_action_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎵 Նոր երգ")],
        [
            KeyboardButton(text="🔙 Տրամադրության մենյու"),
            KeyboardButton(text="🏠 Գլխավոր մենյու"),
        ],
    ],
    resize_keyboard=True,
)


gpt_reply_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
        [KeyboardButton(text="🧹 Մաքրել զրույցը")],
    ],
    resize_keyboard=True,
)


movie_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎭 Ժանրով առաջարկներ"),
            KeyboardButton(text="🔥 Լավագույն 10 ֆիլմ"),
        ],
        [
            KeyboardButton(text="🎞 Ֆիլմի նկարագրություն"),
            KeyboardButton(text="🔍 Ասա ֆիլմի անունը"),
        ],
        [KeyboardButton(text="🎲 Պատահական ֆիլմ")],
        [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)


series_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎭 Սերիալ ըստ ժանրի"),
            KeyboardButton(text="🔥 Լավագույն 10 սերիալ"),
        ],
        [
            KeyboardButton(text="📘 Սերիալի նկարագրություն"),
            KeyboardButton(text="🔍 Ասա սերիալի անունը"),
        ],
        [KeyboardButton(text="🎲 Պատահական սերիալ")],
        [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)

film_and_series_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎥 Ֆիլմեր")],
        [KeyboardButton(text="📺 Սերիալներ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)

movie_genre_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎬 Ակցիա"), KeyboardButton(text="😂 Կատակերգություն")],
        [KeyboardButton(text="😱 Սարսափ"), KeyboardButton(text="🎭 Դրամա")],
        [
            KeyboardButton(text="💘 Ռոմանտիկա"),
            KeyboardButton(text="🕵️ Միստիկա / Թրիլեր"),
        ],
        [KeyboardButton(text="🚀 Գիտաֆանտաստիկա"), KeyboardButton(text="🧙 Ֆանտազիա")],
        [KeyboardButton(text="🎥 Պատմական"), KeyboardButton(text="👨‍👩‍👧 Ընտանեկան")],
        [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)

series_genre_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎭 Դրամա"), KeyboardButton(text="😂 Կատակերգություն")],
        [KeyboardButton(text="🚀 Գիտաֆանտաստիկա"), KeyboardButton(text="🧙 Ֆանտազիա")],
        [KeyboardButton(text="😱 Սարսափ"), KeyboardButton(text="🕵️ Թրիլեր")],
        [KeyboardButton(text="💘 Ռոմանտիկա"), KeyboardButton(text="👨‍👩‍👧 Ընտանեկան")],
        [KeyboardButton(text="🎬 Պատմական"), KeyboardButton(text="🧩 Միստիկա")],
        [KeyboardButton(text="🔙 Վերադառնալ Ֆիլմեր և Սերիալներ")],
        [KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")],
    ],
    resize_keyboard=True,
)

img_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔝 Վերադառնալ գլխավոր մենյու")]]
)
