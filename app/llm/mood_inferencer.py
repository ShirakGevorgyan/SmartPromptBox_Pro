"""Mood-based content generators and parsing/cleanup helpers backed by OpenAI.

Includes small utilities to:
- ask the Chat Completions API with Armenian prompts,
- parse/clean structured outputs (lists/JSON),
- derive songs/movies/quotes/image-prompts for a given mood.
"""

from openai import OpenAI
import re
import os
import ast
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def clean_gpt_code_block(text: str) -> str:
    """Strip surrounding Markdown code fences like ``` or ```python … ``` if present.

    Args:
        text: Raw string that may include a fenced code block.

    Returns:
        The inner content without the code fence markers, trimmed.
    """
    return re.sub(r"```(?:python)?\s*([\s\S]*?)\s*```", r"\1", text).strip()


def parse_fallback_list(response: str) -> List[Dict[str, str]]:
    """Parse a simple 'Artist - Title' list into a structured list of dicts.

    This is used as a fallback when LLM doesn't return valid Python/JSON.

    Args:
        response: Free-form text where each item may look like "Artist - Title".

    Returns:
        List of dicts with keys: title, artist, description, youtube.
        Description and youtube are left minimal/empty in this fallback.
    """
    lines = response.splitlines()
    fallback = []
    for line in lines:
        if " - " in line:
            parts = [p.strip() for p in line.split(" - ", 1)]
            if len(parts) == 2:
                fallback.append(
                    {
                        "title": parts[1],
                        "artist": parts[0],
                        "description": "Նկարագրություն չկա։",
                        "youtube": "",
                    }
                )
    return fallback


def generate_songs_for_mood(mood: str) -> List[Dict[str, str]]:
    """Return 5 songs matching the given mood as a list of dicts.

    The function asks the LLM for a Python `list[dict]` payload and attempts to
    `ast.literal_eval` it. If parsing fails, we fall back to `parse_fallback_list`.

    Args:
        mood: Mood label to guide the LLM (Armenian or English).

    Returns:
        List of song dicts with fields: title, artist, description, youtube.
    """
    system_prompt = (
        "Դու երաժշտական օգնական ես։ "
        f"Օգտատերը նշել է իր տրամադրությունը՝ '{mood}'։ "
        "Առաջարկիր 5 երգ, որոնք համապատասխանում են այդ տրամադրությանը։ "
        "Յուրաքանչյուր երգի համար վերադարձրու հետևյալ դաշտերը՝ title, artist, description, youtube։ "
        "Վերադարձը կառուցիր որպես Python list[dict] այս ձևաչափով՝\n\n"
        "[\n"
        "  {\n"
        '    "title": "Hello",\n'
        '    "artist": "Adele",\n'
        '    "description": "Մելանխոլիկ բալլադ զղջման և կորցրած կապի մասին։",\n'
        '    "youtube": "https://www.youtube.com/watch?v=YQHsXMglC9A"\n'
        "  },\n"
        "  ...\n"
        "]\n\n"
        "Մի՛ գրիր բացատրություններ, միայն ցուցակը՝ կոդի բլոկի մեջ։"
    )

    response = ask_gpt(system_prompt, mood)
    cleaned = clean_gpt_code_block(response)

    try:
        return ast.literal_eval(cleaned)
    except Exception as e:
        print("❌ GPT structured վերադարձը ձախողվեց:", e)
        return parse_fallback_list(response)


def generate_songs_random() -> List[Dict[str, str]]:
    """Return a small list of random songs with light popularity constraints.

    Asks the LLM for a Python `list[dict]`. Falls back to a best-effort parser
    when the response is not valid Python.
    """
    system_prompt = (
        "Դու երաժշտական օգնական ես։ "
        "Օգտատերը նշել է որ ուզում է պատահական (Random) երգ։ "
        "Թող դա լինի այնպիսի երգ որ Youtube-ում ունենա 300 միլիոնից քիչ, շատ քիչ դիտում։ "
        "Երգի համար վերադարձրու հետևյալ դաշտերը՝ title, artist, description, youtube։ "
        "Վերադարձը կառուցիր որպես Python list[dict] այս ձևաչափով՝\n\n"
        "[\n"
        "  {\n"
        '    "title": "Hello",\n'
        '    "artist": "Adele",\n'
        '    "description": "Մելանխոլիկ բալլադ զղջման և կորցրած կապի մասին։",\n'
        '    "youtube": "https://www.youtube.com/watch?v=YQHsXMglC9A"\n'
        "  },\n"
        "  ...\n"
        "]\n\n"
        "Մի՛ գրիր բացատրություններ, միայն ցուցակը՝ կոդի բլոկի մեջ։"
    )

    response = ask_gpt(system_prompt, "")

    cleaned = clean_gpt_code_block(response)

    try:
        return ast.literal_eval(cleaned)
    except Exception as e:
        print("❌ GPT structured վերադարձը ձախողվեց:", e)
        return parse_fallback_list(response)


def generate_movies_for_mood(mood: str) -> list[dict]:
    """Return 5 movie suggestions for a mood as a list of JSON-like dicts.

    Attempts to coerce the response to valid JSON by swapping quotes when needed.

    Args:
        mood: Mood label.

    Returns:
        list[dict]: Each movie dict is expected to contain title, genre, director,
        trailer_url, watch_url. Empty list on failure.
    """
    system_prompt = (
        "Դու կինոյի փորձագետ ես։ "
        f"Օգտատերը ասել է, որ իրեն զգում է՝ '{mood}'։ "
        "Առաջարկիր 5 ֆիլմ՝ հարմար այդ տրամադրությանը։ Յուրաքանչյուր ֆիլմի համար վերադարձրու JSON օբյեկտ՝ հետևյալ դաշտերով՝\n"
        "- title (ֆիլմի անունը)\n"
        "- genre (ժանրը)\n"
        "- director (ռեժիսոր)\n"
        "- trailer_url (YouTube տրեյլերի հղում)\n"
        "- watch_url (IMDB կամ այլ վստահելի դիտելու հղում)\n\n"
        "Վերադարձրու Python list՝ որի ներսում կլինեն այդ 5 ફિલ્મերի JSON օբյեկտները։\n"
        "Ոչ մի բացատրություն մի՛ ավելացրու։ Միայն JSON։"
    )

    response = ask_gpt(system_prompt, mood)
    cleaned = clean_gpt_code_block(response)

    try:
        fixed_json = cleaned.replace("'", '"')
        return json.loads(fixed_json)
    except Exception as e:
        print("❌ GPT վերադարձը չի կարող վերածվել structured ֆիլմերի ցուցակի:", e)
        return []


def generate_quotes_for_mood(mood: str) -> str:
    """Return five short quotes suitable for the user's current mood.

    Args:
        mood: Mood label.

    Returns:
        Raw text with quotes (LLM-generated).
    """
    system_prompt = (
        "Օգտատերը իրեն զգում է՝ '{}'. "
        "Առաջարկիր 5 ներշնչող կամ իմաստալից մեջբերումներ, որոնք կօգնեն նրան այդ զգացողության դեպքում։"
    ).format(mood)

    return ask_gpt(system_prompt, mood)


def generate_image_prompts_for_mood(mood: str) -> str:
    """Return two Armenian TTI prompts tailored to the mood (as plain text).

    Args:
        mood: Mood label.

    Returns:
        Raw text that should contain two prompts, one per line (LLM-generated).
    """
    system_prompt = (
        "Դու արվեստի օգնական ես, ով ստեղծում է նկարների նկարագրություններ (prompt): "
        "Օգտատերը հայտնել է իր տրամադրությունը՝ '{}'. "
        "Առաջարկիր 2 նկարագրություն, որոնք հնարավոր կլինի օգտագործել DALL·E կամ Stable Diffusion-ի միջոցով նկար ստեղծելու համար։"
    ).format(mood)

    return ask_gpt(system_prompt, mood)


def ask_gpt(system_prompt: str, mood: str) -> str:
    """Thin wrapper around OpenAI Chat Completions for Armenian prompts.

    Args:
        system_prompt: System role content.
        mood: Mood string passed as the user message content.

    Returns:
        The LLM's text content, stripped. On error, an Armenian 'error' string.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Ես հիմա զգում եմ՝ {mood}"},
            ],
            temperature=0.9,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT սխալ՝ {e}"


def clean_gpt_descriptions(text: str) -> List[str]:
    """Extract numbered one-line descriptions from an LLM answer.

    Strips code fences, splits by lines, and returns the part after the numbering.

    Args:
        text: Raw LLM text.

    Returns:
        List of cleaned description lines.
    """
    raw = re.sub(r"```(?:python)?\s*([\s\S]*?)\s*```", r"\1", text).strip()
    lines = raw.splitlines()
    return [line.split(". ", 1)[-1].strip() for line in lines if line.strip()]


def describe_songs_llm(song_titles: List[str]) -> List[str]:
    """Ask the LLM to write one-sentence descriptions for each given song title.

    Args:
        song_titles: List of song titles (optionally including artist).

    Returns:
        List of one-line descriptions (same order as input).
    """
    prompt = (
        "Տրված են երգերի անուններ։ Յուրաքանչյուր երգի համար գրիր մի նախադասությամբ նկարագրություն։ "
        "Նկարագրությունը թող լինի տրամադրության, թեմատիկայի կամ ժանրի մասին։ "
        "Պատասխանը վերադարձրու թվագրված ցուցակով՝ օրինակ՝\n"
        "1. Coldplay - Fix You — Հույսի ու վերականգնման մասին մոտիվացիոն երգ։\n\n"
    )

    for i, title in enumerate(song_titles, 1):
        prompt += f"{i}. {title}\n"

    response = ask_gpt(prompt, "")
    return clean_gpt_descriptions(response)
