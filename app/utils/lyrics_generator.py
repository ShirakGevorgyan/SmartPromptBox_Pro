import os
from openai import OpenAI
from dotenv import load_dotenv
from app.scraper.lyrics_scraper import fetch_lyrics_from_genius, clean_lyrics
from app.utils.file_writer import save_as_txt_and_pdf 

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_lyrics(title: str, artist: str) -> str:
#     try:
#         prompt = f"Write full lyrics for the song titled '{title}' by the artist '{artist}'."
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful and creative lyrics generator."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.9,
#             max_tokens=800
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         print(f"OpenAI API Error: {e}")
#         raw_lyrics = fetch_lyrics_from_genius(title, artist)
#         clean = clean_lyrics(raw_lyrics)
#         return clean
def generate_lyrics(title: str, artist: str) -> str:
    try:
        prompt = f"Write full lyrics for the song titled '{title}' by the artist '{artist}'."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and creative lyrics generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=800
        )
        lyrics = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        raw_lyrics = fetch_lyrics_from_genius(title, artist)
        lyrics = clean_lyrics(raw_lyrics)

    # ✅ Պահպանում ենք որպես TXT և PDF
    filename = f"{title}_{artist}".replace(" ", "_")
    save_as_txt_and_pdf(lyrics, filename)

    return lyrics