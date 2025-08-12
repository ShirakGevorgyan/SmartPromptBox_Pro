"""Series suggestions via OpenAI with Armenian prompts.

Functions here mirror the movie helpers but target TV series:
- get_random_series_llm: propose a random series across random genres/years.
- suggest_series_by_description_llm: one series by free-text description.
- get_series_details_by_name_llm: detailed info for a given series title.
- get_series_by_genre_llm: three series for a genre.
- get_top_10_series_llm: a top-10 list of modern series.

All functions send Armenian prompts; plots are refined via `replace_plot_with_refined`.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import random
from app.llm.text_utils import replace_plot_with_refined

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_random_series_llm() -> str:
    """Return a single random series suggestion (genres/years chosen randomly).

    Returns:
        A formatted Armenian block with title, genre, director, cast, plot, rating, links.
    """
    genres = [
        "դրամա",
        "կատակերգություն",
        "գիտաֆանտաստիկա",
        "միստիկա",
        "հոգեբանական թրիլլեր",
        "դետեկտիվ",
        "սարսափ",
        "ֆանտազիա",
        "ռոմանտիկ",
        "պատմական",
        "կրիմինալ",
        "մուլտսերիալ",
        "ֆանտաստիկա",
        "մարդկային հարաբերություններ",
        "կենսագրական",
        "ընտանեկան",
        "դիսթոպիա",
        "սոցիալական դրամա",
        "սպորտային",
        "քաղաքական թրիլլեր",
    ]

    selected_genres = random.sample(genres, k=random.choice([2, 3]))
    genres_str = ", ".join(selected_genres)

    random_start_year = random.choice(range(1980, 2020))
    random_end_year = random.choice(range(random_start_year + 1, 2024))

    prompt_variants = [
        "առաջարկիր սերիալ, որը շատերին դուր կգա",
        "նշիր գերազանց սերիալ՝ ըստ ժանրի և տարեթվի",
        "պատահական, բայց հանրահայտ սերիալի առաջարկ",
        "սերիալ, որն արժե դիտել ըստ ժանրերի",
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
        presence_penalty=1.0,
    )
    raw_output = response.choices[0].message.content
    return replace_plot_with_refined(raw_output, client)


def suggest_series_by_description_llm(description: str) -> str:
    """Suggest a series that fits the provided free-text description.

    Args:
        description: Armenian description of desired theme/mood.

    Returns:
        A formatted Armenian block with standard fields and refined plot.
    """
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
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.7
    )
    raw_output = response.choices[0].message.content
    return replace_plot_with_refined(raw_output, client)


def get_series_details_by_name_llm(series_name: str) -> str:
    """Return a detailed card for the provided series title.

    Args:
        series_name: Series name provided by the user.

    Returns:
        A formatted Armenian block with title, meta fields, refined plot and links.
    """
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

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        raw_output = response.choices[0].message.content
        return replace_plot_with_refined(raw_output, client)

    except Exception:
        return f"Հնարավոր չէ ստանալ տվյալներ «{series_name}» սերիալի մասին այս պահին։"


def get_series_by_genre_llm(genre: str) -> str:
    """Return three series suggestions constrained to a specific genre.

    Args:
        genre: Armenian genre name.

    Returns:
        A formatted Armenian block with three series; plot is refined.
    """
    prompt = f"""
Օգտատերը ընտրել է սերիալի ժանրը՝ {genre}։

Առաջարկիր 3 սերիալ այդ ժանրով՝ տարբեր տարիներից։

Յուրաքանչյուր սերիալի համար տուր հետևյալ կառուցվածքով՝

🎥 Վերնագիր՝ ... (Տարի)
🎭 Ժանրը՝ {genre}
🎬 Ռեժիսոր՝ ...
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)
📜 Սյուժե՝ ...
📊 IMDb գնահատական՝ ...
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)

Մի գրիր բացատրություն։ Մի՛ ավելացրու emojis։
"""
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.85
    )
    raw_output = response.choices[0].message.content
    return replace_plot_with_refined(raw_output, client)


def get_top_10_series_llm() -> str:
    """Return a curated list of ten notable modern series across genres/countries.

    Returns:
        A formatted Armenian block with 10 series and refined plot sections.
    """
    prompt = """
Նշի 10 սերիալ, որոնք համարվում են ժամանակակից լավագույններից։

Նշիր տարբեր ժանրերից, տարբեր երկրներից։ Յուրաքանչյուր սերիալի համար տուր հետևյալ կառուցվածքով՝

🎥 Վերնագիր՝ ... (Տարի)
🎭 Ժանրը՝ ...
🎬 Ռեժիսոր՝ ...
🎭 Դերասաններ՝ ... (ճշգրիտ 5 հայտնի դերասան՝ անուն, ազգանուն ձևաչափով)
📜 Սյուժե՝ ...
📊 IMDb գնահատական՝ ...
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](...)
🎞️ Դիտելու հղում՝ [IMDB կամ այլ վստահելի աղբյուր](...)

Մի՛ գրիր բացատրություն։ Մի՛ ավելացրու emojis (արդենկա)։
"""
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.75
    )
    raw_output = response.choices[0].message.content
    return replace_plot_with_refined(raw_output, client)
