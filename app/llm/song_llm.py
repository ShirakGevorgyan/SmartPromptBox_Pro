import os
import ast
from openai import OpenAI
from typing import List, Dict
from app.llm.mood_inferencer import ask_gpt, clean_gpt_code_block, parse_fallback_list

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_songs_by_genre(genre: str) -> List[Dict[str, str]]:
    system_prompt = (
        "Դու երաժշտական օգնական ես։ "
        f"Օգտատերը նշել է ոճ՝ {genre}։ "
        "Վերադարձիր 5 երգ, որոնց տվյալ ոճը ներկայացված է լավագույն ձևով։ "
        "Յուրաքանչյուր երգի համար վերադարձիր հետևյալ դաշտերը՝ title, artist, description, youtube։ "
        "Վերադարձը կառուցիր որպես Python list[dict]՝ այս ձևաչափով՝\n\n"
        '[\n'
        '  {\n'
        '    "title": "Shape of You",\n'
        '    "artist": "Ed Sheeran",\n'
        '    "description": "Ռիթմիկ փոփ երգ սիրային պատմության մասին։",\n'
        '    "youtube": "https://www.youtube.com/watch?v=JGwWNGJdvx8"\n'
        '  },\n'
        '  ...\n'
        ']\n\n'
        "Մի՛ գրիր բացատրություններ, միայն ցուցակը՝ կոդի բլոկի մեջ։"
    )

    response = ask_gpt(system_prompt, "")
    cleaned = clean_gpt_code_block(response)

    try:
        return ast.literal_eval(cleaned)
    except Exception as e:
        print("❌ Genre LLM structured վերադարձը ձախողվեց:", e)
        return parse_fallback_list(response)


def generate_songs_by_description(description: str) -> List[Dict[str, str]]:
    system_prompt = (
        "Դու երաժշտական օգնական ես։ "
        f"Օգտատերը ցանկանում է երգեր հետևյալ նկարագրության հիման վրա՝\n\"{description}\"։ "
        "Վերադարձիր 2 երգ՝ համապատասխան տրամադրությամբ։ "
        "Յուրաքանչյուր երգի համար վերադարձիր՝ title, artist, description, youtube։ "
        "Ցուցակը վերադարձրու Python list[dict] ձևով՝\n\n"
        '[\n'
        '  {\n'
        '    "title": "...",\n'
        '    "artist": "...",\n'
        '    "description": "...",\n'
        '    "youtube": "..." \n'
        '  },\n'
        '  ...\n'
        ']\n\n'
        "Մի՛ գրիր բացատրություն, միայն ցուցակը՝ կոդի բլոկի մեջ։"
    )

    response = ask_gpt(system_prompt, "")
    cleaned = clean_gpt_code_block(response)

    try:
        return ast.literal_eval(cleaned)
    except Exception as e:
        print("❌ Description LLM structured վերադարձը ձախողվեց:", e)
        return parse_fallback_list(response)


def generate_top_songs_by_artist(artist: str) -> List[Dict[str, str]]:
    system_prompt = (
        "Դու երաժշտական օգնական ես։ "
        f"Օգտատերը ցանկանում է տեսնել «{artist}» արտիստի 10 լավագույն երգերը։ "
        "Յուրաքանչյուր երգի համար վերադարձիր՝ title, artist, description, youtube։ "
        "Ցուցակը վերադարձրու Python list[dict] ձևով՝\n\n"
        '[\n'
        '  {\n'
        '    "title": "...",\n'
        '    "artist": "...",\n'
        '    "description": "...",\n'
        '    "youtube": "..." \n'
        '  },\n'
        '  ...\n'
        ']\n\n'
        "Մի՛ գրիր բացատրություն, միայն ցուցակը՝ կոդի բլոկի մեջ։"
    )

    response = ask_gpt(system_prompt, "")
    cleaned = clean_gpt_code_block(response)

    try:
        return ast.literal_eval(cleaned)
    except Exception as e:
        print("❌ Artist LLM structured վերադարձը ձախողվեց:", e)
        return parse_fallback_list(response)
