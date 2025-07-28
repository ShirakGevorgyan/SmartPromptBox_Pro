import pytest
from unittest.mock import AsyncMock, patch
from aiogram.fsm.context import FSMContext

from app.telegram_bot.handlers import random_songs_handler


@pytest.mark.asyncio
async def test_random_song_handler_success():
    # Create mock Message
    mock_message = AsyncMock()
    mock_message.answer = AsyncMock()

    # Create mock FSM state
    mock_state = AsyncMock(spec=FSMContext)

    mock_songs = [
        {
            "title": "Song 1",
            "artist": "Artist 1",
            "description": "Nice vibe",
            "youtube": "https://youtube.com/1",
        },
        {
            "title": "Song 2",
            "artist": "Artist 2",
            "description": "Chill mood",
            "youtube": "https://youtube.com/2",
        }
    ]

    with patch("app.telegram_bot.handlers.random_songs_handler.generate_songs_random", return_value=mock_songs):
        await random_songs_handler.random_song_handler(mock_message, mock_state)

    assert mock_message.answer.call_count >= 3
    mock_state.update_data.assert_called_once_with(songs_for_download=mock_songs)


@pytest.mark.asyncio
async def test_random_song_handler_empty():
    mock_message = AsyncMock()
    mock_message.answer = AsyncMock()

    mock_state = AsyncMock(spec=FSMContext)

    with patch("app.telegram_bot.handlers.random_songs_handler.generate_songs_random", return_value=[]):
        await random_songs_handler.random_song_handler(mock_message, mock_state)

    mock_message.answer.assert_any_call("❌ Չհաջողվեց գտնել երգ։ Փորձիր նորից 😢")
