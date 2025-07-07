from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from yt_dlp import YoutubeDL
from app.utils.lyrics_generator import generate_lyrics

router = APIRouter()

class YouTubeURL(BaseModel):
    url: str

@router.post("/")
def generate_from_youtube(data: YouTubeURL):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'no_warnings': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url.strip(), download=False)
            title = info.get("title", "Unknown Title")
            channel = info.get("uploader", "Unknown Channel")

            # ✅ Նոր տարբերակ՝ փոխանցում ենք նաև YouTube հղումը
            lyrics = generate_lyrics(title, channel, youtube_url=data.url)

            return {
                "title": title,
                "channel": channel,
                "original_url": data.url,
                "lyrics": lyrics
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid YouTube link or fetch error: {str(e)}")
