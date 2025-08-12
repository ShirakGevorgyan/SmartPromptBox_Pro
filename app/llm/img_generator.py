import os
import uuid
from pathlib import Path
from typing import Final

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_TIMEOUT: Final[int] = 15  # sec
CHUNK_SIZE: Final[int] = 8192
IMAGES_DIR = Path("images")


def _download_image(image_url: str, file_path: Path) -> None:
    with requests.get(image_url, timeout=DEFAULT_TIMEOUT, stream=True) as resp:
        resp.raise_for_status()
        with file_path.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)


def generate_image(prompt: str) -> str:
    """
    Generates an image via OpenAI and saves it into ./images/.
    Returns the file path as string on success, or '' on failure.
    """
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )
        image_url = response.data[0].url

        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        file_path = IMAGES_DIR / f"{uuid.uuid4().hex}.png"

        _download_image(image_url, file_path)
        return str(file_path)

    except Exception as e:
        try:
            if "file_path" in locals():
                fp = Path(file_path)
                if fp.exists():
                    fp.unlink()
        except FileNotFoundError:
            print("ℹ️ Cleanup skipped: file already removed")
        except Exception as cleanup_err:
            print(f"⚠️ Cleanup failed: {cleanup_err}")

        print(f"❌ Error: {e}")
        return ""
