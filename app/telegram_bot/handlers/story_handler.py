# app/telegram_bot/handlers/story_handler.py

import os
import openai
from aiogram import Router
from aiogram.types import Message

router = Router()
openai.api_key = os.getenv("OPENAI_API_KEY")
story_state = {}

def generate_continuation(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Դու պատմող ես, որը ստեղծագործ շարունակում է պատմությունները։"},
                {"role": "user", "content": f"Շարունակիր այս պատմությունը՝ {prompt}"},
            ],
            max_tokens=300,
            temperature=0.9,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT սխալ՝ {e}"

@router.message(lambda msg: msg.text == "✍️ Շարունակիր պատմությունը")
async def ask_for_story(message: Message):
    story_state[message.from_user.id] = True
    await message.answer("📜 Գրիր պատմության սկիզբը, և ես այն կշարունակեմ 🧠")

@router.message()
async def handle_story(message: Message):
    user_id = message.from_user.id
    if story_state.get(user_id):
        prompt = message.text.strip()
        await message.answer("⏳ Շարունակում եմ պատմությունը...")
        continuation = generate_continuation(prompt)
        await message.answer(f"📖 Ահա շարունակությունը՝\n\n{continuation}")
        story_state[user_id] = False
