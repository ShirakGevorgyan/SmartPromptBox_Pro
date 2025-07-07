import os
import uuid
import logging
from yt_dlp import YoutubeDL

TEMP_DIR = "app/temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def sanitize_filename(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in " .-_").strip()

def download_audio(url: str) -> str:
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

        artist = info.get("uploader", "Unknown")
        title = info.get("title", "Untitled")
        clean_name = sanitize_filename(f"{artist} - {title}")
        final_path = os.path.join(TEMP_DIR, clean_name + ".mp3")

        os.rename(mp3_file, final_path)
        logging.info(f"✅ Audio renamed to: {final_path}")
        return final_path

    except Exception as e:
        logging.exception("Audio download failed:")
        raise RuntimeError("❌ Աուդիոն ներբեռնել չհաջողվեց։")

def download_video(url: str, quality: str) -> str:
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

        artist = info.get("uploader", "Unknown")
        title = info.get("title", "Untitled")
        clean_name = sanitize_filename(f"{artist} - {title}")
        final_path = os.path.join(TEMP_DIR, clean_name + ".mp4")

        os.rename(video_file, final_path)
        logging.info(f"✅ Video renamed to: {final_path}")
        return final_path

    except Exception as e:
        logging.exception("Video download failed:")
        raise RuntimeError("❌ Վիդեոն ներբեռնել չհաջողվեց։")
