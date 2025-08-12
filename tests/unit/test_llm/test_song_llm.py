import pytest
from unittest.mock import patch

from app.llm import song_llm


@pytest.fixture
def fake_song_list_response():
    return """```python
[
    {
    "title": "Shape of You",
    "artist": "Ed Sheeran",
    "description": "Ռիթմիկ փոփ երգ սիրային պատմության մասին։",
    "youtube": "https://www.youtube.com/watch?v=JGwWNGJdvx8"
    },
    {
    "title": "Blinding Lights",
    "artist": "The Weeknd",
    "description": "Սինթուեյվ ոճի երգ, լի էներգիայով։",
    "youtube": "https://www.youtube.com/watch?v=4NRXx6U8ABQ"
    }
]
```"""


@patch("app.llm.song_llm.ask_gpt")
def test_generate_songs_by_genre(mock_ask_gpt, fake_song_list_response):
    mock_ask_gpt.return_value = fake_song_list_response
    result = song_llm.generate_songs_by_genre("Pop")
    assert isinstance(result, list)
    assert len(result) >= 2
    assert result[0]["artist"] == "Ed Sheeran"


@patch("app.llm.song_llm.ask_gpt")
def test_generate_songs_by_description(mock_ask_gpt, fake_song_list_response):
    mock_ask_gpt.return_value = fake_song_list_response
    result = song_llm.generate_songs_by_description(
        "փափուկ երաժշտություն անձրևային օրվա համար"
    )
    assert isinstance(result, list)
    assert "title" in result[0]
    assert "youtube" in result[1]


@patch("app.llm.song_llm.ask_gpt")
def test_generate_top_songs_by_artist(mock_ask_gpt, fake_song_list_response):
    mock_ask_gpt.return_value = fake_song_list_response
    result = song_llm.generate_top_songs_by_artist("The Weeknd")
    assert isinstance(result, list)
    assert result[1]["artist"] == "The Weeknd"
    assert result[0]["title"] == "Shape of You"
