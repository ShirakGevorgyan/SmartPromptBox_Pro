import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.telegram_bot.handlers.series_menu_handler import (
    send_random_series,
    handle_description,
    handle_series_name,
    handle_series_genre
)

@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.series_menu_handler.get_random_series_llm")
async def test_send_random_series(mock_random_series_llm):
    mock_random_series_llm.return_value = (
        "🎥 Վերնագիր՝ Dark (2017)\n"
        "🎭 Ժանրը՝ Mystery\n"
        "🎬 Ռեժիսոր՝ Baran bo Odar\n"
        "🎭 Դերասաններ՝ Louis Hofmann, Lisa Vicari, ...\n"
        "📜 Սյուժե՝ ...\n"
        "📊 IMDb գնահատական՝ 8.7\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://www.imdb.com)"
    )

    mock_msg = AsyncMock(spec=Message)
    mock_msg.answer = AsyncMock()

    await send_random_series(mock_msg)

@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.series_menu_handler.suggest_series_by_description_llm")
async def test_handle_description(mock_suggest_llm):
    mock_suggest_llm.return_value = (
        "🎥 Վերնագիր՝ The Crown (2016)\n"
        "🎭 Ժանրը՝ Drama\n"
        "🎬 Ռեժիսոր՝ Peter Morgan\n"
        "🎭 Դերասաններ՝ Claire Foy, Matt Smith, ...\n"
        "📜 Սյուժե՝ ...\n"
        "📊 IMDb գնահատական՝ 8.6\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://www.imdb.com)"
    )

    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "Բրիտանական թագավորական ընտանիքի մասին սերիալ"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.clear = AsyncMock()

    await handle_description(mock_msg, mock_state)

@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.series_menu_handler.get_series_details_by_name_llm")
async def test_handle_series_name(mock_series_details):
    mock_series_details.return_value = (
        "🎥 Վերնագիր՝ Breaking Bad (2008)\n"
        "🎭 Ժանրը՝ Crime, Drama\n"
        "🎬 Ռեժիսոր՝ Vince Gilligan\n"
        "🎭 Դերասաններ՝ Bryan Cranston, Aaron Paul, ...\n"
        "📊 IMDb գնահատական՝ 9.5\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://www.imdb.com)"
    )

    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "Breaking Bad"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.clear = AsyncMock()

    await handle_series_name(mock_msg, mock_state)

@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.series_menu_handler.get_series_by_genre_llm")
async def test_handle_series_genre_valid(mock_genre_llm):
    mock_genre_llm.return_value = (
        "🎥 Վերնագիր՝ Chernobyl (2019)\n"
        "🎭 Ժանրը՝ Historical\n"
        "🎬 Ռեժիսոր՝ Johan Renck\n"
        "🎭 Դերասաններ՝ Jared Harris, Stellan Skarsgård, ...\n"
        "📜 Սյուժե՝ ...\n"
        "📊 IMDb գնահատական՝ 9.4\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://www.imdb.com)"
    )

    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "🎬 Պատմական"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.set_state = AsyncMock()

    await handle_series_genre(mock_msg, mock_state)

@pytest.mark.asyncio
async def test_handle_series_genre_invalid():
    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "🎸 Ռոք"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)

    await handle_series_genre(mock_msg, mock_state)
