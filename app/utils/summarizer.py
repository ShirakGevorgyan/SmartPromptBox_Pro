import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def summarize_history(history):
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    prompt = f"Ամփոփիր այս GPT և օգտատիրոջ զրույցը՝ 2-3 նախադասությամբ:\n\n{history_text}\n\n✅ Ամփոփում՝"

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()
