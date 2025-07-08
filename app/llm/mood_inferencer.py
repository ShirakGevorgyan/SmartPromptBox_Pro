from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_songs_for_mood(mood: str) -> str:
    system_prompt = (
        "Դու երաժշտական օգնական ես։ "
        "Օգտատերը նշել է իր տրամադրությունը՝ '{}'. "
        "Առաջարկիր 5 երգ, որոնք համապատասխանում են այդ զգացողությանը։"
    ).format(mood)

    return ask_gpt(system_prompt, mood)


# ✅ 5 Ֆիլմ տրամադրությանը համապատասխան
def generate_movies_for_mood(mood: str) -> str:
    system_prompt = (
        "Դու կինոյի փորձագետ ես։ "
        "Օգտատերը իրեն զգում է՝ '{}'. "
        "Առաջարկիր 5 ֆիլմ, որոնք կհամապատասխանեն այդ տրամադրությանը։"
    ).format(mood)

    return ask_gpt(system_prompt, mood)


# ✅ 5 մեջբերում տրամադրությանը համապատասխան
def generate_quotes_for_mood(mood: str) -> str:
    system_prompt = (
        "Օգտատերը իրեն զգում է՝ '{}'. "
        "Առաջարկիր 5 ներշնչող կամ իմաստալից մեջբերումներ, որոնք կօգնեն նրան այդ զգացողության դեպքում։"
    ).format(mood)

    return ask_gpt(system_prompt, mood)


# ✅ 2 նկարագրություն՝ text-to-image-ի համար
def generate_image_prompts_for_mood(mood: str) -> str:
    system_prompt = (
        "Դու արվեստի օգնական ես, ով ստեղծում է նկարների նկարագրություններ (prompt): "
        "Օգտատերը հայտնել է իր տրամադրությունը՝ '{}'. "
        "Առաջարկիր 2 նկարագրություն, որոնք հնարավոր կլինի օգտագործել DALL·E կամ Stable Diffusion-ի միջոցով նկար ստեղծելու համար։"
    ).format(mood)

    return ask_gpt(system_prompt, mood)


# 🧠 Ընդհանուր GPT հարցման ֆունկցիա
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