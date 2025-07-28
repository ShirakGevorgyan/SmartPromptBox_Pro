from unittest.mock import patch, MagicMock
from app.llm import image_generator


# ✅ Test 1: generate_image_prompts_from_mood
@patch("app.llm.image_generator.client")
def test_generate_image_prompts_from_mood(mock_client):
    # Mock GPT response
    mock_response_text = """1. A lonely tree standing in the fog at dawn.  
2. A person walking alone under heavy rain with neon lights reflecting on wet streets."""
    
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=mock_response_text))
    ]

    prompts = image_generator.generate_image_prompts_from_mood("melancholic")
    assert isinstance(prompts, list)
    assert len(prompts) == 2
    assert "fog" in prompts[0] or "rain" in prompts[1]


# ✅ Test 2: generate_images_from_prompts
@patch("app.llm.image_generator.client")
def test_generate_images_from_prompts(mock_client):
    prompts = ["A cozy cabin in snowy mountains", "Sunset over a calm ocean"]

    # Mock DALL·E image response
    mock_client.images.generate.return_value.data = [
        MagicMock(url="https://fakeimage1.com")
    ]

    results = image_generator.generate_images_from_prompts(prompts)

    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0][0] == "A cozy cabin in snowy mountains"
    assert results[0][1].startswith("https://")
