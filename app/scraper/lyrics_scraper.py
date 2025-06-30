import os
import lyricsgenius
from dotenv import load_dotenv
import re
import logging

load_dotenv()
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

def clean_title(title: str) -> str:
    cleaned = re.sub(r"[\(\[].*?[\)\]]", "", title)
    return cleaned.strip()


genius_client = lyricsgenius.Genius(
    GENIUS_ACCESS_TOKEN,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    timeout=15,  
    retries=3,
    sleep_time=0.5,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

def fetch_lyrics_from_genius(title: str, artist: str) -> str:
    try:
        if not GENIUS_ACCESS_TOKEN:
            return "Missing Genius Access Token."

        clean_title_text = clean_title(title)

        song = genius_client.search_song(clean_title_text, artist)
        if song and song.lyrics:
            return song.lyrics
        return "Lyrics not found from Genius."
    except Exception as e:
        logging.error(f"Genius lyrics fetching error: {e}")
        return f"Error fetching lyrics from Genius: {str(e)}"
    

def clean_lyrics(raw_lyrics: str) -> str:
    """
    Մաքրում է երգի բառերը՝ սկսելով [Intro]-ից,
    հեռացնում Contributors, Translations, լեզուների անուններ, ու դարձնում մաքուր տող առ տող։
    """

    # Գտնում ենք [Intro]-ից սկսվող հատվածը
    intro_match = re.search(r"\[Intro\].*", raw_lyrics, re.DOTALL | re.IGNORECASE)
    if not intro_match:
        # Եթե չկա [Intro], սկսում ենք ամբողջ տեքստից
        lyrics_section = raw_lyrics
    else:
        lyrics_section = intro_match.group(0)

    # Հեռացնում ենք Contributors-ով սկսվող ավելորդ բոլոր տվյալները՝ ամբողջ վերջը
    lyrics_section = re.split(r"ContributorsTranslations", lyrics_section, flags=re.IGNORECASE)[0]

    # Հեռացնում ենք լեզուների ցուցակները, եթե մնացել են
    lyrics_section = re.sub(r"((Türkçe|Português|Italiano|Español|Deutsch|Français|Русский|Українська).*)", "", lyrics_section, flags=re.DOTALL | re.IGNORECASE)

    # Հեռացնում ենք բոլոր [Intro], [Verse], [Chorus], [Bridge], [Outro], [Pre-Chorus] տեքստերը (եթե չես ուզում թողնել)
    lyrics_section = re.sub(r"\[[^\]]+\]", "", lyrics_section)

    # Հեռացնում ենք ավելորդ դատարկ տողերը և սպեյսերը տողերի սկզբից և վերջից
    lines = [line.strip() for line in lyrics_section.splitlines() if line.strip()]

    # Միավորում ենք մաքուր տողերը նոր տողերով
    clean_text = "\n".join(lines)

    return clean_text