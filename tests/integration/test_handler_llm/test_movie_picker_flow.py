import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.telegram_bot.handlers.movie_menu_handler import (
    send_random_movie,
    handle_description,
    handle_movie_name,
    handle_movie_genre,
)


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.movie_menu_handler.get_random_movie_llm")
async def test_send_random_movie(mock_random_movie_llm):
    mock_random_movie_llm.return_value = (
        "🎥 Վերնագիր` Interstellar (2014)\n"
        "🎭 Ժանրը՝ Sci-Fi\n"
        "🎬 Ռեժիսոր՝ Christopher Nolan\n"
        "🎭 Դերասաններ՝ Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine, Matt Damon\n"
        "📜 Սյուժե՝ ...\n"
        "📊 IMDb գնահատական՝ 8.6\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://www.imdb.com)"
    )

    mock_msg = AsyncMock(spec=Message)
    mock_msg.answer = AsyncMock()

    await send_random_movie(mock_msg)


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.movie_menu_handler.suggest_movies_by_description_llm")
async def test_handle_description(mock_suggest_movies):
    mock_suggest_movies.return_value = (
        "🎥 Վերնագիր` Titanic (1997)\n"
        "🎭 Ժանրը՝ Romance\n"
        "🎬 Ռեժիսոր՝ James Cameron\n"
        "🎭 Դերասաններ՝ Leonardo DiCaprio, Kate Winslet, ...\n"
        "📊 IMDb գնահատական՝ 7.8\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://www.imdb.com)"
    )

    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "Ցանկանում եմ սիրային դրամա"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.clear = AsyncMock()

    await handle_description(mock_msg, mock_state)


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.movie_menu_handler.get_movie_details_by_name_llm")
async def test_handle_movie_name(mock_movie_details):
    mock_movie_details.return_value = (
        "🎥 Վերնագիր` Inception (2010)\n"
        "🎭 Ժանրը՝ Sci-Fi\n"
        "🎬 Ռեժիսոր՝ Christopher Nolan\n"
        "🎭 Դերասաններ՝ ...\n"
        "📊 IMDb գնահատական՝ 8.8\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://www.imdb.com)"
    )

    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "Inception"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.clear = AsyncMock()

    await handle_movie_name(mock_msg, mock_state)


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.movie_menu_handler.get_movies_by_genre_llm")
async def test_handle_movie_genre_valid(mock_by_genre):
    mock_by_genre.return_value = (
        "🎥 Վերնագիր` Gladiator (2000)\n"
        "🎭 Ժանրը՝ Action\n"
        "🎬 Ռեժիսոր՝ Ridley Scott\n"
        "🎭 Դերասաններ՝ Russell Crowe, Joaquin Phoenix, ...\n"
        "📊 IMDb գնահատական՝ 8.5\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://www.imdb.com)"
    )

    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "🎬 Ակցիա"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.clear = AsyncMock()

    await handle_movie_genre(mock_msg, mock_state)


@pytest.mark.asyncio
async def test_handle_movie_genre_invalid():
    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "🎸 Ռոք"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.clear = AsyncMock()

    await handle_movie_genre(mock_msg, mock_state)
