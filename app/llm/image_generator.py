"""Helpers to generate image prompts and images via OpenAI."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_image_prompts_from_mood(mood: str) -> list[str]:
    """Return two short, TTI-friendly Armenian prompts derived from a mood.

    The prompts are intended for text-to-image models (e.g., DALL·E, SD).

    Args:
        mood: A mood label (e.g., "happy", "sad", "neutral", or Armenian text).

    Returns:
        list[str]: Up to two cleaned, succinct prompts.
        On error, the list contains a single error message.
    """
    system_prompt = (
        f"Օգտատերը զգում է '{mood}' տրամադրություն։ "
        f"Առաջարկիր 2 նկարների պարզ նկարագրություն՝ որոնք հնարավոր է օգտագործել text-to-image մոդելներով, "
        f"օրինակ՝ DALL·E կամ Stable Diffusion։ Պահպանիր պարզ, հստակ ու նկարագրական ոճ, առանց վերնագրերի։"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Ես հիմա զգում եմ՝ {mood}"},
            ],
            temperature=0.8,
        )
        content = response.choices[0].message.content.strip()

        lines = []
        for line in content.split("\n"):
            line = line.strip("•- ")
            if not line:
                continue
            if ":" in line:
                parts = line.split(":", 1)
                line = parts[1].strip()
            lines.append(line)

        return lines[:2]

    except Exception as e:
        return [f"❌ Սխալ՝ {str(e)}"]


def generate_images_from_prompts(prompts: list[str]) -> list[tuple[str, str]]:
    """Generate images for each prompt and return (prompt, image_url) pairs.

    Args:
        prompts: A list of textual prompts.

    Returns:
        list[tuple[str, str]]: For each input prompt, a 2-tuple of
        `(original_prompt, image_url_or_error)`. Errors are returned as text.
    """
    results = []
    for prompt in prompts:
        try:
            image_resp = client.images.generate(
                model="dall-e-3", prompt=prompt, n=1, size="1024x1024"
            )
            image_url = image_resp.data[0].url
            results.append((prompt.strip(), image_url))
        except Exception as e:
            results.append((prompt.strip(), f"❌ Սխալ՝ {str(e)}"))
    return results
