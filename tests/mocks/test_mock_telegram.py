import pytest
from unittest.mock import AsyncMock, patch
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup

from app.telegram_bot.handlers.series_menu_handler import (
    show_series_menu,
    send_random_series,
    handle_description,
)


@pytest.mark.asyncio
async def test_show_series_menu_sends_correct_message():
    message = AsyncMock()
    message.text = "📺 Սերիալներ"
    message.answer = AsyncMock()

    await show_series_menu(message)

    message.answer.assert_called_once()
    args, kwargs = message.answer.call_args
    assert "📺 Ընտրիր գործողությունը" in args[0]


@pytest.mark.asyncio
async def test_show_series_menu_reply_markup_buttons():
    message = AsyncMock()
    message.text = "📺 Սերիալներ"
    message.answer = AsyncMock()

    await show_series_menu(message)

    message.answer.assert_called_once()
    _, kwargs = message.answer.call_args
    reply_markup: ReplyKeyboardMarkup = kwargs.get("reply_markup")
    assert isinstance(reply_markup, ReplyKeyboardMarkup)

    all_button_texts = [button.text for row in reply_markup.keyboard for button in row]

    expected_buttons = [
        "🎭 Սերիալ ըստ ժանրի",
        "🔥 Լավագույն 10 սերիալ",
        "📘 Սերիալի նկարագրություն",
        "🔍 Ասա սերիալի անունը",
        "🎲 Պատահական սերիալ",
        "🔙 Վերադառնալ Ֆիլմեր և Սերիալներ",
        "🔝 Վերադառնալ գլխավոր մենյու",
    ]

    for expected in expected_buttons:
        assert expected in all_button_texts, f"Missing button: {expected}"


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.series_menu_handler.get_random_series_llm")
@patch(
    "app.telegram_bot.handlers.series_menu_handler.send_long_message",
    new_callable=AsyncMock,
)
async def test_send_random_series_mocked_gpt(mock_send_long, mock_gpt):
    message = AsyncMock()
    message.text = "🎲 Պատահական սերիալ"
    message.answer = AsyncMock()

    mock_gpt.return_value = (
        "🎥 Վերնագիր՝ Breaking Bad (2008)\n"
        "🎭 Ժանրը՝ Drama\n"
        "🎬 Ռեժիսոր՝ Vince Gilligan\n"
        "🎭 Դերասաններ՝ Bryan Cranston, Aaron Paul\n"
        "📜 Սյուժե՝ ...\n"
        "📊 IMDb գնահատական՝ 9.5\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtu.be/xyz)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://imdb.com)"
    )

    await send_random_series(message)

    mock_gpt.assert_called_once()
    mock_send_long.assert_called_once()
    message.answer.assert_called()


@pytest.mark.asyncio
@patch(
    "app.telegram_bot.handlers.series_menu_handler.suggest_series_by_description_llm"
)
@patch(
    "app.telegram_bot.handlers.series_menu_handler.send_long_message",
    new_callable=AsyncMock,
)
async def test_handle_description_sets_state_and_replies(
    mock_send_long, mock_suggest_llm
):
    mock_state = AsyncMock(spec=FSMContext)
    message = AsyncMock()
    message.text = "ուզում եմ դրամատիկ ու հուզիչ սերիալ"
    message.answer = AsyncMock()

    mock_suggest_llm.return_value = (
        "🎥 Վերնագիր՝ This Is Us (2016)\n"
        "🎭 Ժանրը՝ Drama\n"
        "🎬 Ռեժիսոր՝ ...\n"
        "🎭 Դերասաններ՝ ...\n"
        "📜 Սյուժե՝ ...\n"
        "📊 IMDb գնահատական՝ 8.7\n"
        "▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtu.be/abc)\n"
        "🎞️ Դիտելու հղում՝ [IMDB](https://imdb.com)"
    )

    await handle_description(message, mock_state)

    mock_suggest_llm.assert_called_once_with("ուզում եմ դրամատիկ ու հուզիչ սերիալ")
    mock_send_long.assert_called_once()
    mock_state.clear.assert_called_once()
    message.answer.assert_called()
