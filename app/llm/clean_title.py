from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def clean_song_title_llm(original_title: str) -> str:
    prompt = f"""
You are a music metadata expert with knowledge of song names, artists, and common YouTube title structures.

Given the following noisy or incomplete YouTube video title:

"{original_title}"

Your task is:
- Remove redundant words like "official video", "lyrics", "visualizer", "HD", "Live" etc.
- If artist name is repeated, keep only once.
- If only the song title is provided and artist is missing, intelligently guess the artist if possible (based on the name and your prior knowledge).
- Return the final clean title in the format: Artist - Song Title

Return only the cleaned title without any explanation.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
