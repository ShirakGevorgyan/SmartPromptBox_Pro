import pytest
from unittest.mock import patch

from app.llm import mood_inferencer


@pytest.fixture
def fake_song_response():
    return """```python
[
    {
    "title": "Fix You",
    "artist": "Coldplay",
    "description": "Երգ հույսի և վերականգնման մասին։",
    "youtube": "https://youtu.be/k4V3Mo61fJM"
    },
    {
    "title": "Someone Like You",
    "artist": "Adele",
    "description": "Սրտաճմլիկ բալլադ կորուսյալ սիրո մասին։",
    "youtube": "https://youtu.be/hLQl3WQQoQ0"
    }
]
```"""


def test_clean_gpt_code_block():
    raw = "```python\nprint('Hello')\n```"
    result = mood_inferencer.clean_gpt_code_block(raw)
    assert "print" in result
    assert "```" not in result


def test_parse_fallback_list_parses_correctly():
    response = "Adele - Hello\nColdplay - Fix You"
    fallback = mood_inferencer.parse_fallback_list(response)
    assert len(fallback) == 2
    assert fallback[0]["title"] == "Hello"
    assert fallback[0]["artist"] == "Adele"


@patch("app.llm.mood_inferencer.ask_gpt")
def test_generate_songs_for_mood_parses_valid(mock_ask_gpt, fake_song_response):
    mock_ask_gpt.return_value = fake_song_response
    result = mood_inferencer.generate_songs_for_mood("հուսահատ")
    assert isinstance(result, list)
    assert result[0]["title"] == "Fix You"


@patch("app.llm.mood_inferencer.ask_gpt")
def test_generate_movies_for_mood(mock_ask_gpt):
    raw_json = """[
    {
        "title": "The Pursuit of Happyness",
        "genre": "Drama",
        "director": "Gabriele Muccino",
        "trailer_url": "https://youtu.be/89Kq8SDyvfg",
        "watch_url": "https://www.imdb.com/title/tt0454921/"}
    ]"""
    mock_ask_gpt.return_value = raw_json
    result = mood_inferencer.generate_movies_for_mood("տխուր")
    assert isinstance(result, list)
    assert result[0]["title"] == "The Pursuit of Happyness"


@patch("app.llm.mood_inferencer.ask_gpt")
def test_describe_songs_llm(mock_ask_gpt):
    gpt_text = """```1. Adele - Hello. Սրտաշարժ երգ սիրո կորուստի մասին։
2. Coldplay - Fix You. Երգ հույսի ու վերականգնման մասին։```"""
    mock_ask_gpt.return_value = gpt_text

    result = mood_inferencer.describe_songs_llm(["Adele - Hello", "Coldplay - Fix You"])
    assert len(result) == 2
    assert "սիրո կորուստի" in result[0]
