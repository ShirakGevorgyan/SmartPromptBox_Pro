import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import uuid

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_image(prompt: str) -> str:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        image_url = response.data[0].url

        file_path = f"images/{uuid.uuid4().hex}.png"
        os.makedirs("images", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(requests.get(image_url).content)

        return file_path
    except Exception as e:
        print(f"❌ Error: {e}")
        return ""
