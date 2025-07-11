import os
import uuid
import logging

from yt_dlp import YoutubeDL
from app.llm.clean_title import clean_song_title_llm

TEMP_DIR = "app/temp"
os.makedirs(TEMP_DIR, exist_ok=True)


# ✅ Օգնական՝ ֆայլանվան մաքրում
def sanitize_filename(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in " .-_").strip()


# ✅ Ընդհանուր աուդիո ներբեռնող՝ ըստ YouTube հղման
def download_audio(url: str, filename: str = None) -> str:
    try:
        temp_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True,
            'no_warnings': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            base = ydl.prepare_filename(info)
            mp3_file = os.path.splitext(base)[0] + ".mp3"

        if not os.path.exists(mp3_file):
            raise FileNotFoundError(f"Audio file not found: {mp3_file}")

        if filename:
            clean_name = sanitize_filename(filename)
        else:
            artist = info.get("uploader", "Unknown")
            title = info.get("title", "Untitled")
            clean_name = sanitize_filename(f"{artist} - {title}")

        final_path = os.path.join(TEMP_DIR, clean_name + ".mp3")
        os.rename(mp3_file, final_path)

        logging.info(f"✅ Audio renamed to: {final_path}")
        return final_path

    except Exception:
        logging.exception("Audio download failed:")
        raise RuntimeError("❌ Աուդիոն ներբեռնել չհաջողվեց։")


# ✅ Ընդհանուր վիդեո ներբեռնող՝ ըստ YouTube հղման և որակի
def download_video(url: str, quality: str, filename: str = None) -> str:
    try:
        temp_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.%(ext)s")

        ydl_opts = {
            'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
            'outtmpl': temp_filename,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            base = ydl.prepare_filename(info)
            video_file = os.path.splitext(base)[0] + ".mp4"

        if not os.path.exists(video_file):
            raise FileNotFoundError(f"Video file not found: {video_file}")

        if filename:
            clean_name = sanitize_filename(filename)
        else:
            artist = info.get("uploader", "Unknown")
            title = info.get("title", "Untitled")
            clean_name = sanitize_filename(f"{artist} - {title}")

        final_path = os.path.join(TEMP_DIR, clean_name + ".mp4")
        os.rename(video_file, final_path)

        logging.info(f"✅ Video renamed to: {final_path}")
        return final_path

    except Exception:
        logging.exception("Video download failed:")
        raise RuntimeError("❌ Վիդեոն ներբեռնել չհաջողվեց։")


# ✅ Mood/GPT հիմքով երգի անվանումով lyrics տարբերակ ներբեռնելու ֆունկցիա
def download_audio_by_song_name(song_title: str) -> str:
    """
    Ներբեռնում է երգի ամենավստահելի lyrics տարբերակը՝ ըստ GPT-ի մաքրված անունի։
    """
    try:
        clean_title = clean_song_title_llm(song_title)
        search_query = f"ytsearch10:{clean_title} lyrics"
        temp_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_filename,
            'quiet': True,
            'no_warnings': True,
            'match_filter': lambda info: None if "lyrics" in info.get("title", "").lower() else "Not a lyrics version",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }


        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            base = ydl.prepare_filename(info)
            mp3_file = os.path.splitext(base)[0] + ".mp3"

        if not os.path.exists(mp3_file):
            raise FileNotFoundError("Lyrics audio not found.")

        clean_name = sanitize_filename(clean_title)
        final_path = os.path.join(TEMP_DIR, clean_name + ".mp3")
        os.rename(mp3_file, final_path)

        logging.info(f"🎵 Lyrics audio downloaded: {final_path}")
        return final_path

    except Exception:
        logging.exception("Lyrics audio download failed:")
        raise RuntimeError(f"❌ `{song_title}` երգի lyrics տարբերակը ներբեռնել չհաջողվեց։")
