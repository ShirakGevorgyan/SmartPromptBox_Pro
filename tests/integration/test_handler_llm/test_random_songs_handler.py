import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.telegram_bot.handlers.random_songs_handler import (
    handle_genre_input,
    handle_description_input,
    handle_artist_input,
)


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.random_songs_handler.generate_songs_by_genre")
async def test_handle_genre_input_valid(mock_genre_llm):
    mock_genre_llm.return_value = [
        {
            "title": "Shape of You",
            "artist": "Ed Sheeran",
            "description": "Ռիթմիկ փոփ երգ սիրային պատմության մասին։",
            "youtube": "https://youtube.com",
        }
    ]

    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "🎶 Փոփ"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.update_data = AsyncMock()
    mock_state.clear = AsyncMock()
    mock_state.set_state = AsyncMock()

    await handle_genre_input(mock_msg, mock_state)


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.random_songs_handler.generate_songs_by_description")
async def test_handle_description_input(mock_desc_llm):
    mock_desc_llm.return_value = [
        {
            "title": "Let Her Go",
            "artist": "Passenger",
            "description": "Տխուր բալլադ, կորուստի և կարոտի մասին։",
            "youtube": "https://youtube.com",
        }
    ]

    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "Տխուր սիրո երգ"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.update_data = AsyncMock()
    mock_state.clear = AsyncMock()
    mock_state.set_state = AsyncMock()

    await handle_description_input(mock_msg, mock_state)


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.random_songs_handler.generate_top_songs_by_artist")
async def test_handle_artist_input(mock_artist_llm):
    mock_artist_llm.return_value = [
        {
            "title": "Someone Like You",
            "artist": "Adele",
            "description": "Հզոր վոկալային կատարում կորած սիրո մասին։",
            "youtube": "https://youtube.com",
        }
    ]

    mock_msg = AsyncMock(spec=Message)
    mock_msg.text = "Adele"
    mock_msg.answer = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.update_data = AsyncMock()
    mock_state.clear = AsyncMock()
    mock_state.set_state = AsyncMock()

    await handle_artist_input(mock_msg, mock_state)
