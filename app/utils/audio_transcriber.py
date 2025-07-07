# app/utils/audio_transcriber.py

import os
import subprocess
from yt_dlp import YoutubeDL

TEMP_DIR = "app/temp"

def download_audio_from_youtube(url: str) -> str:
    """
    Բեռնում է YouTube տեսահոլովակից աուդիոն .mp3 ֆորմատով
    """
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(TEMP_DIR, '%(title)s.%(ext)s'),
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
        print(f"✅ Downloaded audio: {filename}")
        return filename  # Վերադարձնում է բեռնված mp3 ֆայլի ուղին

def transcribe_audio(file_path: str, model: str = "small") -> str:
    """
    Տեքստ է ստանում աուդիո ֆայլից՝ Whisper մոդելով (պետք է տեղադրած լինի whisper CLI)
    """
    print(f"📥 Transcribing file: {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Audio file not found: {file_path}")

    try:
        subprocess.run([
            "whisper", file_path,
            "--language", "en",
            "--model", model
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ Whisper CLI failed: {e}")

    txt_path = file_path.rsplit('.', 1)[0] + ".txt"
    print(f"📄 Expected transcript path: {txt_path}")

    if not os.path.exists(txt_path):
        raise FileNotFoundError(f"❌ Transcript file not found: {txt_path}")

    with open(txt_path, "r", encoding="utf-8") as f:
        lyrics = f.read()

    print("✅ Transcription successful")
    return lyrics.strip()
