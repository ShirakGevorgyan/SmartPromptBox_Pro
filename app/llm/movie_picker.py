"""Movie suggestions via OpenAI with Armenian prompts.

Functions here:
- add_default_links_if_missing: ensure trailer/watch links are present.
- get_random_movie_llm: propose a random movie across random genres and years.
- suggest_movies_by_description_llm: one movie based on a free-text description.
- get_movie_details_by_name_llm: detailed info for a given movie title.
- get_movies_by_genre_llm: three movies for a specific genre.
- get_top_10_movies_llm: a top-10 modern cinema list.

All functions call OpenAI Chat (Armenian prompts) and post-process the output
using `replace_plot_with_refined` to rewrite the plot section in clearer Armenian.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import random
from app.llm.text_utils import replace_plot_with_refined

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_TRAILER = "https://youtube.com"
DEFAULT_WATCH = "https://www.imdb.com"


def add_default_links_if_missing(text: str) -> str:
    """Append default trailer/watch links if the response omitted them.

    Args:
        text: Raw LLM response text that should contain trailer/watch links.

    Returns:
        The original text, possibly with appended trailer and watch links.
    """
    if "▶️ Տրեյլեր" not in text:
        text += f"\n▶️ Տրեյլեր՝ [Դիտել YouTube-ում]({DEFAULT_TRAILER})"
    if "🎞️ Դիտելու հղում" not in text:
        text += f"\n🎞️ Դիտելու հղում՝ [IMDB]({DEFAULT_WATCH})"
    return text


# 🎲 Պատահական ֆիլմ
def get_random_movie_llm() -> str:
    """Return a single random movie suggestion (genres/years chosen randomly).

    Builds an Armenian prompt with randomly sampled genres and year range,
    asks OpenAI, injects default links if needed, then refines the '📜 Սյուժե' section.

    Returns:
        A formatted Armenian block with title, genre, director, cast, plot, ratings, etc.
    """
    genres = [
        "գիտաֆանտաստիկա",
        "դրամա",
        "արկածային",
        "կատակերգություն",
        "հոգեբանական թրիլլեր",
        "սարսափ",
        "պատմական",
        "ռոմանտիկ",
        "դետեկտիվ",
        "մյուզիքլ",
        "ակցիան",
        "ֆանտազիա",
        "միստիկա",
        "սպորտային",
        "քրեական",
        "պատերազմական",
        "կենսագրական",
        "ընտանեկան",
        "արևելյան մարտարվեստ",
        "վեստերն",
        "փաստագրական",
        "սոցիալական դրամա",
    ]
    selected_genres = random.sample(genres, k=random.choice([2, 3]))
    genres_str = ", ".join(selected_genres)

    start_year = random.randint(1970, 2020)
    end_year = random.randint(start_year + 1, 2023)

    prompt_intro = random.choice(
        [
            "առաջարկիր մի ֆիլմ, որը շատերը կվայելեն",
            "նշիր հիանալի ֆիլմ՝ ըստ ժանրի և տարեթվի",
            "պատահական, բայց հանրահայտ ֆիլմի առաջարկ",
            "ֆիլմ, որն արժե դիտել ըստ քո ընտրած ժանրերի",
        ]
    )

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
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=1.2
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)


def suggest_movies_by_description_llm(description: str) -> str:
    """Suggest a movie that fits the provided free-text description.

    Args:
        description: Short Armenian description of what the user wants.

    Returns:
        A formatted Armenian block with standard fields and refined plot.
    """
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
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.9
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)


def get_movie_details_by_name_llm(movie_name: str) -> str:
    """Return a detailed card for the provided movie title.

    Args:
        movie_name: Movie name provided by the user.

    Returns:
        A formatted Armenian block with title, meta fields, refined plot and links.
    """
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
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.7
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)


def get_movies_by_genre_llm(genre: str) -> str:
    """Return three movie suggestions constrained to a specific genre.

    Args:
        genre: Armenian genre name.

    Returns:
        A formatted Armenian block with three movies; plot is refined.
    """
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
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.85
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)


def get_top_10_movies_llm() -> str:
    """Return a curated list of ten notable modern films across genres/countries.

    Returns:
        A formatted Armenian block with 10 films and refined plot sections.
    """
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
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.75
    )
    raw_output = response.choices[0].message.content
    text_with_links = add_default_links_if_missing(raw_output)
    return replace_plot_with_refined(text_with_links, client)
