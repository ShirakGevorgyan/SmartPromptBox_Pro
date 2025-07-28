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
    """Հանում է ```python ... ``` պարունակությունը, եթե կա"""
    return re.sub(r"```(?:python)?\s*([\s\S]*?)\s*```", r"\1", text).strip()

def parse_fallback_list(response: str) -> List[Dict[str, str]]:
    lines = response.splitlines()
    fallback = []
    for line in lines:
        if " - " in line:
            parts = [p.strip() for p in line.split(" - ", 1)]
            if len(parts) == 2:
                fallback.append({
                    "title": parts[1],
                    "artist": parts[0],
                    "description": "Նկարագրություն չկա։",
                    "youtube": ""
                })
    return fallback


def generate_songs_for_mood(mood: str) -> List[Dict[str, str]]:
    system_prompt = (
        "Դու երաժշտական օգնական ես։ "
        f"Օգտատերը նշել է իր տրամադրությունը՝ '{mood}'։ "
        "Առաջարկիր 5 երգ, որոնք համապատասխանում են այդ տրամադրությանը։ "
        "Յուրաքանչյուր երգի համար վերադարձրու հետևյալ դաշտերը՝ title, artist, description, youtube։ "
        "Վերադարձը կառուցիր որպես Python list[dict] այս ձևաչափով՝\n\n"
        '[\n'
        '  {\n'
        '    "title": "Hello",\n'
        '    "artist": "Adele",\n'
        '    "description": "Մելանխոլիկ բալլադ զղջման և կորցրած կապի մասին։",\n'
        '    "youtube": "https://www.youtube.com/watch?v=YQHsXMglC9A"\n'
        '  },\n'
        '  ...\n'
        ']\n\n'
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
    system_prompt = (
        "Դու երաժշտական օգնական ես։ "
        "Օգտատերը նշել է որ ուզում է պատահական (Random) երգ։ "
        "Թող դա լինի այնպիսի երգ որ Youtube-ում ունենա 300 միլիոնից քիչ, շատ քիչ դիտում։ "
        "Երգի համար վերադարձրու հետևյալ դաշտերը՝ title, artist, description, youtube։ "
        "Վերադարձը կառուցիր որպես Python list[dict] այս ձևաչափով՝\n\n"
        '[\n'
        '  {\n'
        '    "title": "Hello",\n'
        '    "artist": "Adele",\n'
        '    "description": "Մելանխոլիկ բալլադ զղջման և կորցրած կապի մասին։",\n'
        '    "youtube": "https://www.youtube.com/watch?v=YQHsXMglC9A"\n'
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
        print("❌ GPT structured վերադարձը ձախողվեց:", e)
        return parse_fallback_list(response)

def generate_movies_for_mood(mood: str) -> list[dict]:
    system_prompt = (
        "Դու կինոյի փորձագետ ես։ "
        f"Օգտատերը ասել է, որ իրեն զգում է՝ '{mood}'։ "
        "Առաջարկիր 5 ֆիլմ՝ հարմար այդ տրամադրությանը։ Յուրաքանչյուր ֆիլմի համար վերադարձրու JSON օբյեկտ՝ հետևյալ դաշտերով՝\n"
        "- title (ֆիլմի անունը)\n"
        "- genre (ժանրը)\n"
        "- director (ռեժիսոր)\n"
        "- trailer_url (YouTube տրեյլերի հղում)\n"
        "- watch_url (IMDB կամ այլ վստահելի դիտելու հղում)\n\n"
        "Վերադարձրու Python list՝ որի ներսում կլինեն այդ 5 ֆիլմերի JSON օբյեկտները։\n"
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
    system_prompt = (
        "Օգտատերը իրեն զգում է՝ '{}'. "
        "Առաջարկիր 5 ներշնչող կամ իմաստալից մեջբերումներ, որոնք կօգնեն նրան այդ զգացողության դեպքում։"
    ).format(mood)

    return ask_gpt(system_prompt, mood)


def generate_image_prompts_for_mood(mood: str) -> str:
    system_prompt = (
        "Դու արվեստի օգնական ես, ով ստեղծում է նկարների նկարագրություններ (prompt): "
        "Օգտատերը հայտնել է իր տրամադրությունը՝ '{}'. "
        "Առաջարկիր 2 նկարագրություն, որոնք հնարավոր կլինի օգտագործել DALL·E կամ Stable Diffusion-ի միջոցով նկար ստեղծելու համար։"
    ).format(mood)

    return ask_gpt(system_prompt, mood)


def ask_gpt(system_prompt: str, mood: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Ես հիմա զգում եմ՝ {mood}"}
            ],
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT սխալ՝ {e}"
    
    

def clean_gpt_descriptions(text: str) -> List[str]:
    """Մաքրում է GPT վերադարձած կոդաբլոկը և առանձնացնում միայն նկարագրությունները"""
    raw = re.sub(r"```(?:python)?\s*([\s\S]*?)\s*```", r"\1", text).strip()
    lines = raw.splitlines()
    return [line.split(". ", 1)[-1].strip() for line in lines if line.strip()]

def describe_songs_llm(song_titles: List[str]) -> List[str]:
    """Ստանում է երգերի անունների լիստ և վերադարձնում է նկարագրությունների լիստ"""
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
