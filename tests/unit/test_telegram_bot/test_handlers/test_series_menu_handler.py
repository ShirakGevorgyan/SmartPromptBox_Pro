# tests/unit/test_telegram_bot/test_handlers/test_series_menu_handler.py

import pytest
import warnings
from unittest.mock import AsyncMock, patch
from app.telegram_bot.handlers import series_menu_handler


@pytest.mark.asyncio
async def test_send_random_series():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning, message="The `__fields__` attribute is deprecated.*")

        fake_message = AsyncMock()
        with patch("app.telegram_bot.handlers.series_menu_handler.get_random_series_llm") as mock_llm:
            mock_llm.return_value = (
                "🎥 Վերնագիր՝ Test Series\n"
                "🎭 Ժանրը՝ Drama\n"
                "🎬 Ռեժիսոր՝ Someone\n"
                "🎭 Դերասաններ՝ A, B, C\n"
                "📜 Սյուժե՝ Lorem ipsum\n"
                "📊 IMDb գնահատական՝ 9.1\n"
                "Տրեյլեր՝ [YouTube](https://youtube.com)\n"
                "Դիտելու հղում՝ [Link](https://example.com)"
            )
            await series_menu_handler.send_random_series(fake_message)
            fake_message.answer.assert_called()


@pytest.mark.asyncio
async def test_handle_description():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning, message="The `__fields__` attribute is deprecated.*")

        fake_message = AsyncMock()
        fake_state = AsyncMock()
        fake_message.text = "Funny sci-fi with robots"
        with patch("app.telegram_bot.handlers.series_menu_handler.suggest_series_by_description_llm") as mock_llm:
            mock_llm.return_value = (
                "🎥 Վերնագիր՝ Robo Laughs\n"
                "🎭 Ժանրը՝ Comedy, Sci-Fi\n"
                "🎬 Ռեժիսոր՝ Jane Doe\n"
                "🎭 Դերասաններ՝ X, Y, Z\n"
                "📜 Սյուժե՝ Robots invade comedy club\n"
                "📊 IMDb գնահատական՝ 8.5\n"
                "Տրեյլեր՝ [Trailer](https://youtube.com)\n"
                "Դիտելու հղում՝ [Watch](https://example.com)"
            )
            await series_menu_handler.handle_description(fake_message, fake_state)
            fake_message.answer.assert_called()


@pytest.mark.asyncio
async def test_handle_series_name():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning, message="The `__fields__` attribute is deprecated.*")

        fake_message = AsyncMock()
        fake_state = AsyncMock()
        fake_message.text = "Breaking Bad"
        with patch("app.telegram_bot.handlers.series_menu_handler.get_series_details_by_name_llm") as mock_llm:
            mock_llm.return_value = (
                "🎥 Վերնագիր՝ Breaking Bad\n"
                "🎭 Ժանրը՝ Crime, Drama\n"
                "🎬 Ռեժիսոր՝ Vince Gilligan\n"
                "🎭 Դերասաններ՝ Bryan, Aaron\n"
                "📜 Սյուժե՝ Chemistry teacher turns to crime\n"
                "📊 IMDb գնահատական՝ 9.5\n"
                "Տրեյլեր՝ [Trailer](https://youtube.com)\n"
                "Դիտելու հղում՝ [Watch](https://example.com)"
            )
            await series_menu_handler.handle_series_name(fake_message, fake_state)
            fake_message.answer.assert_called()
