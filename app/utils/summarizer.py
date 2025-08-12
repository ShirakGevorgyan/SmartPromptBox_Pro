import os
from openai import AsyncOpenAI
from functools import lru_cache
from dotenv import load_dotenv


@lru_cache()
def get_openai_client() -> AsyncOpenAI:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is missing.")
    return AsyncOpenAI(api_key=api_key)


async def summarize_history(history):
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    prompt = f"Ամփոփիր այս GPT և օգտատիրոջ զրույցը՝ 2-3 նախադասությամբ:\n\n{history_text}\n\n✅ Ամփոփում՝"

    client = get_openai_client()

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()
