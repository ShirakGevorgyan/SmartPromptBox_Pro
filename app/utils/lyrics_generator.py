# app/utils/lyrics_generator.py

from dotenv import load_dotenv
from app.utils.file_writer import save_as_txt_and_pdf
from app.utils.audio_transcriber import download_audio_from_youtube, transcribe_audio
from app.scraper.musixmatch_scraper import fetch_lyrics_sync




load_dotenv()

def generate_lyrics(title: str, artist: str, youtube_url: str = None) -> str:
    lyrics = None
    error_source = None

    # ✅ Փորձում ենք Musixmatch ուղղակի կայքից
    try:
        lyrics = fetch_lyrics_sync(title, artist)
        print("✅ Lyrics fetched from Musixmatch (direct)")
    except Exception as e:
        print(f"Musixmatch fetch error: {e}")
        error_source = "musixmatch"

    # ❌ Եթե Musixmatch-ից չստացվեց, անցնում ենք Whisper
    if not lyrics and youtube_url:
        try:
            audio_path = download_audio_from_youtube(youtube_url)
            lyrics = transcribe_audio(audio_path)
            print("✅ Lyrics transcribed via Whisper")
        except Exception as e:
            print(f"Whisper transcription error: {e}")
            error_source = "whisper"

    if not lyrics:
        lyrics = f"❌ Unable to fetch lyrics using {error_source}."

    filename = f"{title}_{artist}".replace(" ", "_")
    save_as_txt_and_pdf(lyrics, filename)

    return lyrics
