"""Chat history summarization via OpenAI (Armenian output).

Provides a cached `AsyncOpenAI` client and a single `summarize_history` function
that condenses a list of role/content messages into a short 2–3 sentence summary.
"""

import os
from openai import AsyncOpenAI
from functools import lru_cache
from dotenv import load_dotenv


@lru_cache()
def get_openai_client() -> AsyncOpenAI:
    """Return a cached AsyncOpenAI client initialized from `OPENAI_API_KEY`.

    Raises:
        RuntimeError: if the environment variable is missing.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is missing.")
    return AsyncOpenAI(api_key=api_key)


async def summarize_history(history):
    """Summarize a chat history into 2–3 Armenian sentences.

    Args:
        history: Iterable of dicts with keys `role` and `content`.

    Returns:
        A short Armenian summary as plain text (string).
    """
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
