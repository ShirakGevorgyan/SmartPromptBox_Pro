from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.lyrics_generator import generate_lyrics 
import logging

router = APIRouter()

class SongInfo(BaseModel):
    title: str
    artist: str

@router.post("/")
def generate_song_lyrics(data: SongInfo):
    try:
        lyrics = generate_lyrics(data.title, data.artist)
        return {
            "title": data.title,
            "artist": data.artist,
            "lyrics": lyrics
        }
    except Exception as e:
        logging.error(f"Error generating lyrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate lyrics.")