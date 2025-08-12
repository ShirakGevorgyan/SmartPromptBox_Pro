# tests/test_movie_menu_handler.py

from app.telegram_bot.handlers.movie_menu_handler import (
    extract_links_from_text,
    clean_llm_text,
    split_movies,
)


def test_extract_links_from_text():
    text = (
        "🎥 Վերնագիր: Some Movie\n"
        "▶️ Տրեյլեր՝ [Watch Trailer](https://youtube.com/watch?v=abc123)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://www.imdb.com/title/tt1234567/)"
    )
    trailer, watch = extract_links_from_text(text)
    assert trailer == "https://youtube.com/watch?v=abc123"
    assert watch == "https://www.imdb.com/title/tt1234567/"


def test_extract_links_from_text_missing_links():
    text = "🎥 Վերնագիր: Some Movie\nNo links provided"
    trailer, watch = extract_links_from_text(text)
    assert trailer == "https://youtube.com"
    assert watch == "https://www.imdb.com"


def test_clean_llm_text():
    text = (
        "🎥 Վերնագիր: Some Movie\n"
        "▶️ Տրեյլեր՝ [Watch Trailer](https://youtube.com)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://imdb.com)"
    )
    cleaned = clean_llm_text(text)
    assert "Տրեյլեր" not in cleaned
    assert "Դիտելու հղում" not in cleaned
    assert "🎥 Վերնագիր" in cleaned


def test_split_movies():
    input_text = (
        "🎥 Վերնագիր: Movie 1\nSome details\n"
        "🎥 Վերնագիր: Movie 2\nOther details\n"
        "🎥 Վերնագիր: Movie 3\nMore details"
    )
    result = split_movies(input_text)
    assert len(result) == 3
    assert result[0].startswith("🎥 Վերնագիր: Movie 1")
    assert result[1].startswith("🎥 Վերնագիր: Movie 2")
    assert result[2].startswith("🎥 Վերնագիր: Movie 3")
