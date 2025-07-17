from openai import OpenAI
import os
from dotenv import load_dotenv
import random
from app.llm.text_utils import replace_plot_with_refined

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🎲 1. Պատահական սերիալ
def get_random_series_llm() -> str:
    genres = [
        "դրամա", "կատակերգություն", "գիտաֆանտաստիկա", "միստիկա", "հոգեբանական թրիլլեր",
        "դետեկտիվ", "սարսափ", "ֆանտազիա", "ռոմանտիկ", "պատմական", "կրիմինալ",
        "մուլտսերիալ", "ֆանտաստիկա", "մարդկային հարաբերություններ", "կենսագրական",
        "ընտանեկան", "դիսթոպիա", "սոցիալական դրամա", "սպորտային", "քաղաքական թրիլլեր"
    ]

    selected_genres = random.sample(genres, k=random.choice([2, 3]))
    genres_str = ", ".join(selected_genres)

    random_start_year = random.choice(range(1980, 2020))
    random_end_year = random.choice(range(random_start_year + 1, 2024))

    prompt_variants = [
        "առաջարկիր սերիալ, որը շատերին դուր կգա",
        "նշիր գերազանց սերիալ՝ ըստ ժանրի և տարեթվի",
        "պատահական, բայց հանրահայտ սերիալի առաջարկ",
        "սերիալ, որն արժե դիտել ըստ ժանրերի"
    ]
    prompt_intro = random.choice(prompt_variants)

    prompt = f"""
Խնդրում եմ {prompt_intro}։

Ժանրերը՝ {genres_str}  
Տարեթվերի միջակայք՝ {random_start_year} - {random_end_year}

Տվյալը տուր հետևյալ ձևաչափով՝

🎥 Վերնագիր՝ ... (Տարի)  
🎭 Ժանրը՝ ...  
🎬 Ռեժիսոր՝ ...  
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)  
📜 Սյուժե՝ ...  
📊 IMDb գնահատական՝ ...  
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)  
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)

Մի գրիր բացատրություն։ Միայն սերիալի տվյալները։ Մի՛ ավելացրու emojis (դրանք արդեն կան)։
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=1.0
    )
    raw_output = response.choices[0].message.content
    return replace_plot_with_refined(raw_output, client)


# 🎞 2. Ըստ նկարագրության
def suggest_series_by_description_llm(description: str) -> str:
    prompt = f"""
Օգտատերը ցանկանում է սերիալ առաջարկ՝ ըստ նկարագրության․
«{description}»

Առաջարկիր միայն մեկ սերիալ՝ հետևյալ ձևաչափով՝

🎥 Վերնագիր՝ ... (Տարի)  
🎭 Ժանրը՝ ...  
🎬 Ռեժիսոր՝ ...  
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)  
📜 Սյուժե՝ ...  
📊 IMDb գնահատական՝ ...  
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)  
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)

Մի գրիր բացատրություն։ Միայն սերիալի տվյալները։ Մի՛ ավելացրու emojis (դրանք արդեն կան)։
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    raw_output = response.choices[0].message.content
    return replace_plot_with_refined(raw_output, client)


# 🔍 3. Մանրամասն ինֆո ըստ անվանման
def get_series_details_by_name_llm(series_name: str) -> str:
    prompt = f"""
Օգտատերը գրում է սերիալի անունը՝ «{series_name}»

Խնդրում եմ տուր այս սերիալի մասին ամբողջական ինֆո՝ հետևյալ կառուցվածքով՝

🎥 Վերնագիր՝ ... (Տարի)  
🎭 Ժանրը՝ ...  
🎬 Ռեժիսոր՝ ...  
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)  
💸 Բյուջե՝ ...  
💰 Եկամուտ՝ ...  
📜 Սյուժե՝ ...  
📊 IMDb գնահատական՝ ...  
🤔 Հետաքրքիր փաստ՝ ...  
📢 Արժե՞ դիտել այս սերիալը՝ ...  
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)  
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)

Մի գրիր բացատրություն, մի ավելացրու emojis (արդեն կան)։
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )
    raw_output = response.choices[0].message.content
    return replace_plot_with_refined(raw_output, client)
