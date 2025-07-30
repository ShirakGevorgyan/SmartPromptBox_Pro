import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.telegram_bot.handlers.mood_handler import mood_generate


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.mood_handler.generate_songs_for_mood")
@patch("app.telegram_bot.handlers.mood_handler.send_song_buttons")
async def test_mood_generate_songs(mock_send_song_buttons, mock_generate_songs_for_mood):
    mock_message = MagicMock(spec=Message)
    mock_message.text = "🎵 5 երգ"
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_data = AsyncMock(return_value={"mood": "😢 Տխուր եմ"})

    mock_generate_songs_for_mood.return_value = [
        {
            "title": "Hello",
            "artist": "Adele",
            "description": "Sad song",
            "youtube": "https://youtube.com"
        }
    ]

    await mood_generate(mock_message, mock_state)

    mock_generate_songs_for_mood.assert_called_once_with("😢 Տխուր եմ")
    mock_send_song_buttons.assert_called_once()


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.mood_handler.generate_movies_for_mood")
@patch("app.telegram_bot.handlers.mood_handler.send_movies_as_buttons")
async def test_mood_generate_movies(mock_send_movies_as_buttons, mock_generate_movies_for_mood):
    mock_message = MagicMock(spec=Message)
    mock_message.text = "🎬 5 ֆիլմ"
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_data = AsyncMock(return_value={"mood": "🤩 Ուրախ եմ"})

    mock_generate_movies_for_mood.return_value = [
        {
            "title": "Movie Title",
            "genre": "Comedy",
            "director": "John Doe",
            "trailer_url": "https://youtube.com",
            "watch_url": "https://imdb.com"
        }
    ]

    await mood_generate(mock_message, mock_state)

    mock_generate_movies_for_mood.assert_called_once_with("🤩 Ուրախ եմ")
    mock_send_movies_as_buttons.assert_called_once()


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.mood_handler.generate_quotes_for_mood")
async def test_mood_generate_quotes(mock_generate_quotes_for_mood):
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "💬 5 մեջբերում"
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_data = AsyncMock(return_value={"mood": "😎 Մոտիվացված եմ"})

    mock_generate_quotes_for_mood.return_value = "1. Quote 1\n2. Quote 2"

    await mood_generate(mock_message, mock_state)

    mock_generate_quotes_for_mood.assert_called_once_with("😎 Մոտիվացված եմ")
    mock_message.answer.assert_any_call("1. Quote 1\n2. Quote 2")


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.mood_handler.generate_images_from_prompts")
@patch("app.telegram_bot.handlers.mood_handler.generate_image_prompts_from_mood")
async def test_mood_generate_images(mock_generate_image_prompts_from_mood, mock_generate_images_from_prompts):
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "🖼 2 նկարների նկարագրություն"
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_data = AsyncMock(return_value={"mood": "😐 Ուղղակի լավ եմ"})

    mock_generate_image_prompts_from_mood.return_value = "Prompt text"
    mock_generate_images_from_prompts.return_value = [
        ("Prompt 1", "https://image1.com"),
        ("Prompt 2", "https://image2.com")
    ]

    await mood_generate(mock_message, mock_state)

    mock_generate_image_prompts_from_mood.assert_called_once_with("😐 Ուղղակի լավ եմ")
    mock_generate_images_from_prompts.assert_called_once()
