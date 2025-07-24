from openai import OpenAI
import os
from dotenv import load_dotenv
import random
from app.llm.text_utils import replace_plot_with_refined

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Հավելյալ fallback հղումներ
DEFAULT_TRAILER = "https://youtube.com"
DEFAULT_WATCH = "https://www.imdb.com"

def add_default_links_if_missing(text: str) -> str:
    if "▶️ Տրեյլեր" not in text:
        text += f"\n▶️ Տրեյլեր՝ [Դիտել YouTube-ում]({DEFAULT_TRAILER})"
    if "🎞️ Դիտելու հղում" not in text:
        text += f"\n🎞️ Դիտելու հղում՝ [IMDB]({DEFAULT_WATCH})"
    return text


# 🎲 Պատահական ֆիլմ
def get_random_movie_llm() -> str:
    genres = [
        "գիտաֆանտաստիկա", "դրամա", "արկածային", "կատակերգություն", "հոգեբանական թրիլլեր",
        "սարսափ", "պատմական", "ռոմանտիկ", "դետեկտիվ", "մյուզիքլ", "ակցիան", 
        "ֆանտազիա", "միստիկա", "սպորտային", "քրեական", "պատերազմական", "կենսագրական", 
        "ընտանեկան", "արևելյան մարտարվեստ", "վեստերն", "փաստագրական", "սոցիալական դրամա"
    ]
    selected_genres = random.sample(genres, k=random.choice([2, 3]))
    genres_str = ", ".join(selected_genres)

    start_year = random.randint(1970, 2020)
    end_year = random.randint(start_year + 1, 2023)

    prompt_intro = random.choice([
        "առաջարկիր մի ֆիլմ, որը շատերը կվայելեն",
        "նշիր հիանալի ֆիլմ՝ ըստ ժանրի և տարեթվի",
        "պատահական, բայց հանրահայտ ֆիլմի առաջարկ",
        "ֆիլմ, որն արժե դիտել ըստ քո ընտրած ժանրերի"
    ])

    prompt = f"""
Խնդրում եմ {prompt_intro}։

Ժանրերը՝ {genres_str}  
Տարեթվերի միջակայք՝ {start_year} - {end_year}

Տվյալը տուր հետևյալ ձևաչափով՝

🎥 Վերնագիր` ... (Տարի)  
🎭 Ժանրը՝ ...  
🎬 Ռեժիսոր՝ ...  
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)  
📜 Սյուժե՝ ...  
📊 IMDb գնահատական՝ ...   
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)  
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)


# 🎞 Ըստ նկարագրության
def suggest_movies_by_description_llm(description: str) -> str:
    prompt = f"""
Օգտատերը ցանկանում է ֆիլմ առաջարկ՝ ըստ նկարագրության․
«{description}»

Տվյալը տուր հետևյալ ձևաչափով՝

🎥 Վերնագիր` ... (Տարի)  
🎭 Ժանրը՝ ...  
🎬 Ռեժիսոր՝ ...  
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)  
📊 IMDb գնահատական՝ ...   
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)  
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)


# 🔍 Ըստ անունի
def get_movie_details_by_name_llm(movie_name: str) -> str:
    prompt = f"""
Օգտատերը գրում է ֆիլմի անունը՝ «{movie_name}»

Տվյալը տուր հետևյալ կառուցվածքով՝

🎥 Վերնագիր` ... (Տարի)  
🎭 Ժանրը՝ ...  
🎬 Ռեժիսոր՝ ...  
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)  
💸 Բյուջե՝ ...  
💰 Եկամուտ՝ ...  
📜 Սյուժե՝ ...  
📊 IMDb գնահատական՝ ...  
🤔 Հետաքրքիր փաստ՝ ...  
📢 Արժե՞ դիտել այս ֆիլմը՝ ...  
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)  
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)


def get_movies_by_genre_llm(genre: str) -> str:
    prompt = f"""
Օգտատերը ընտրել է հետևյալ ժանրը՝ {genre}։

Առաջարկիր 3 ֆիլմ այդ ժանրով՝ տարբեր տարիներից։  
Տվյալները տուր յուրաքանչյուր ֆիլմի համար հետևյալ ձևաչափով՝

🎥 Վերնագիր` ... (Տարի)  
🎭 Ժանրը՝ {genre}  
🎬 Ռեժիսոր՝ ...  
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)
📜 Սյուժե՝ ...   
📊 IMDb գնահատական՝ ...   
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)  
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)

Մի՛ գրիր բացատրություններ, տուր ֆիլմերը հաջորդաբար։
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)


# 🔥 Լավագույն 10 ֆիլմ (անկախ ժանրից)
def get_top_10_movies_llm() -> str:
    prompt = """
Առաջարկիր 10 ֆիլմ, որոնք համարվում են ժամանակակից կինոյի լավագույններից։  
Նշի տարբեր ժանրերից, տարբեր երկրներից։  

Յուրաքանչյուր ֆիլմի համար տուր հետևյալ ձևաչափով՝

🎥 Վերնագիր` ... (Տարի)  
🎭 Ժանրը՝ ...  
🎬 Ռեժիսոր՝ ...  
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)
📜 Սյուժե՝ ...   
📊 IMDb գնահատական՝ ...   
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)  
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)

Մի՛ գրիր բացատրություն կամ հավելյալ մեկնաբանություն։ Պարզ ցուցակ ֆիլմերով։
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.75
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)