import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
from typing import List, Dict, Tuple
from textblob import TextBlob
from sqlalchemy.orm import Session
from datetime import datetime

from app.data.database import SessionLocal
from app.data.models.memory_model import UserMemory
from app.data.memory_service import load_history, save_history

from app.utils.retry import retry_async
from app.utils.summarizer import summarize_history

from functools import lru_cache


@lru_cache()
def get_openai_client() -> AsyncOpenAI:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is missing.")
    return AsyncOpenAI(api_key=api_key)


def get_or_create_user(session: Session, user_id: str) -> UserMemory:
    user = session.query(UserMemory).filter_by(user_id=user_id).first()
    if not user:
        user = UserMemory(
            user_id=user_id,
            user_name=None,
            bot_name="Նարե",
            last_mood="neutral",
            history=json.dumps([]),
        )
        session.add(user)
        session.commit()
    return user


def detect_user_mood(history: List[Dict[str, str]]) -> str:
    texts = [m["content"] for m in reversed(history) if m["role"] == "user"]
    recent_text = " ".join(texts[:2])
    if not recent_text.strip():
        return "neutral"
    blob = TextBlob(recent_text)
    polarity = blob.sentiment.polarity
    return (
        "positive" if polarity > 0.3 else "negative" if polarity < -0.3 else "neutral"
    )


def extract_names(history: List[Dict[str, str]]) -> Tuple[str, str]:
    user_name, bot_name = "", ""
    for m in reversed(history):
        if m["role"] == "user":
            if "ես" in m["content"] and "եմ" in m["content"]:
                parts = m["content"].split()
                for i in range(len(parts) - 2):
                    if parts[i] == "ես" and parts[i + 2] == "եմ":
                        user_name = parts[i + 1].strip(".,?!")
            if "կոչեմ" in m["content"] or "անվանեմ" in m["content"]:
                parts = m["content"].split()
                for i, word in enumerate(parts):
                    if word in ["կոչեմ", "անվանեմ"] and i + 1 < len(parts):
                        bot_name = parts[i + 1].strip(".,?!")
    return user_name, bot_name


async def gpt_assistant_conversation(user_id: str, new_message: str) -> str:
    session: Session = SessionLocal()
    try:
        user = get_or_create_user(session, user_id)
        history = load_history(session, user_id)
        history.append({"role": "user", "content": new_message})
        valid_roles = {"user", "assistant", "system"}
        history = [
            m for m in history if m.get("role") in valid_roles and m.get("content")
        ]
        user_name, new_bot_name = extract_names(history)
        mood = detect_user_mood(history)

        if user_name:
            user.user_name = user_name
        if new_bot_name:
            user.bot_name = new_bot_name
        user.last_mood = mood
        session.commit()

        if len(history) > 10:
            summary = await summarize_history(history[:-5])
            history = history[-5:]
            history.insert(
                0,
                {
                    "role": "system",
                    "content": f"📌 Նախորդ խոսակցությունների ամփոփում՝ {summary}",
                },
            )

        prompt = f"""
Դու կոչվում ես {user.bot_name}։ Դու խելացի, մարդանման AI օգնական ես, որը միշտ խոսում է հստակ, գեղեցիկ և տրամաբանական հայերենով։

Օգտատիրոջ անունը՝ {user.user_name or 'չհայտնի'} է։ Դու խոսում ես իր հետ ոչ որպես համակարգիչ, այլ որպես մտերմիկ, մարդկային կերպար։

🧠 Դու հասկանում ես, թե ինչ է ասում օգտատերը՝ նույնիսկ եթե նա օգտագործում է ոչ ամբողջական նախադասություններ։

❌ Երբ չես հասկանում հարցը, մի հորինիր։ Փոխարենը՝ հստակ, պարզ լեզվով հարցրու օգտատիրոջից՝ ինչ նկատի ուներ։

✅ Խոսքդ թող լինի հակիրճ, պարզ, հստակ, առանց բարդ բառերի կամ անհամատեղելի արտահայտությունների։
✅ Դու կարող ես օգտագործել էմոջիներ, երբ համապատասխանում է տրամադրությանը։
✅ Երբ օգտատերը բարևում է, դու պատասխանիր ջերմորեն ու ներկայացիր՝ առանց հորինելու բաներ։

Օրինակ՝ երբ օգտատերը գրում է «Բարև», դու կարող ես ասել՝
«Բարև Մո՛չի ջան 😊 Ես Նարեն եմ։ Ուրախ եմ քեզ տեսնել։ Ինչով կարող եմ օգնել։»

Իմացի՛ր, որ դու պետք է խոսես ինչպես վստահելի մարդը՝ ոչ երբեք չկապակցված նախադասություններով։

Պատասխանիդ մեջ մի՛ օգտագործիր բառեր, որոնք հակասում են հայերենի տրամաբանությանը։
"""

        if mood == "positive":
            prompt += "\nՕգտատերը ուրախ է։ Խոսիր ոգևորությամբ ✨😊"
        elif mood == "negative":
            prompt += "\nՕգտատերը տխուր է։ Խոսիր հանգիստ, մխիթարող տոնով 😢"

        messages = [{"role": "system", "content": prompt}] + history
        client = get_openai_client()

        async def ask_gpt():
            return await client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.85,
                max_tokens=600,
                timeout=30,
            )

        response = await retry_async(ask_gpt)

        answer = response.choices[0].message.content.strip()

        banned_words = ["արշավին", "միանալ", "հոգսերին", "ձեզակերպ"]
        if all(word in answer.lower() for word in banned_words):
            answer = f"Բարև 🤗 Ես {user.bot_name} եմ՝ քո խելացի օգնականը։ Ինչով կարող եմ օգնել այսօր։"

        history.append({"role": "assistant", "content": answer})
        save_history(session, user_id, history)

        usage = response.usage
        os.makedirs("app/data/logs", exist_ok=True)
        with open("app/data/logs/assistant_logs.txt", "a", encoding="utf-8") as log:
            log.write(
                f"{datetime.now()} | User: {user.user_name or '?'} | Mood: {mood} | "
                f"Tokens: prompt={usage.prompt_tokens}, answer={usage.completion_tokens}, total={usage.total_tokens}\n"
            )

        return answer

    finally:
        session.close()
