import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from typing import List, Dict

# Բեռնում ենք .env-ից բանալին
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

# Ֆունկցիա՝ ուղարկում է history + համակարգային հրահանգ
async def gpt_assistant_conversation(history: List[Dict[str, str]]) -> str:
    """
    history = [
        {"role": "user", "content": "Ես Հայոբն եմ"},
        {"role": "assistant", "content": "Ողջույն Հայոբ, ուրախ եմ քեզ տեսնել"},
        ...
    ]
    """
    system_prompt = {
        "role": "system",
        "content": "Դու խելացի, բարեհամբույր և շարունակական հիշողություն ունեցող օգնական ես։"
    }

    messages = [system_prompt] + history

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content
