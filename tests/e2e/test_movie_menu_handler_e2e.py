import pytest
from unittest.mock import patch
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, User, Chat, Update
from datetime import datetime
import copy

from app.telegram_bot.handlers.series_menu_handler import (
    router as series_router_original,
    SeriesStates,
)

mock_series_result = """
🎥 Սերիալ (2021)
🎭 Դրամա
🎬 Ռեժիսոր՝ Jane Doe
🎭 Դերասաններ՝ John, Mary, Ana
📜 Սյուժե՝ Deep and emotional.
📊 IMDb գնահատական՝ 9.0
▶️ Տրեյլեր՝ [Դիտել](https://youtube.com/trailer)
🎞️ Դիտելու հղում՝ [IMDB](https://imdb.com/watch)
⬇️ Ընտրիր հաջորդ քայլը։
"""

def create_bot_and_dispatcher():
    series_router = copy.deepcopy(series_router_original)
    bot = Bot(token="123456:TESTTOKEN", parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(series_router)
    return bot, dp

@pytest.mark.asyncio
async def test_random_series_e2e():
    bot, dp = create_bot_and_dispatcher()
    user = User(id=100, is_bot=False, first_name="Tester")
    chat = Chat(id=100, type="private")
    message = Message(
        message_id=1,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="🎲 Պատահական սերիալ"
    )
    update = Update(update_id=1, message=message)

    with patch("app.telegram_bot.handlers.series_menu_handler.get_random_series_llm", return_value=mock_series_result):
        calls = []
        async def mock_answer(self, text, **kwargs):
            calls.append(text)
        with patch.object(Message, "answer", new=mock_answer):
            await dp.feed_update(bot=bot, update=update)
        assert any("⬇️" in c for c in calls)

@pytest.mark.asyncio
async def test_series_by_description_e2e():
    bot, dp = create_bot_and_dispatcher()
    user = User(id=101, is_bot=False, first_name="Tester")
    chat = Chat(id=101, type="private")
    context = dp.fsm.get_context(bot=bot, user_id=user.id, chat_id=chat.id)
    await context.set_state(SeriesStates.waiting_for_description)

    message = Message(
        message_id=2,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="Something dark and twisted"
    )
    update = Update(update_id=2, message=message)

    with patch("app.telegram_bot.handlers.series_menu_handler.suggest_series_by_description_llm", return_value=mock_series_result):
        calls = []
        async def mock_answer(self, text, **kwargs):
            calls.append(text)
        with patch.object(Message, "answer", new=mock_answer):
            await dp.feed_update(bot=bot, update=update)
        assert any("⬇️" in c for c in calls)

@pytest.mark.asyncio
async def test_series_by_name_e2e():
    bot, dp = create_bot_and_dispatcher()
    user = User(id=102, is_bot=False, first_name="Tester")
    chat = Chat(id=102, type="private")
    context = dp.fsm.get_context(bot=bot, user_id=user.id, chat_id=chat.id)
    await context.set_state(SeriesStates.waiting_for_series_name)

    message = Message(
        message_id=3,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="Breaking Bad"
    )
    update = Update(update_id=3, message=message)

    with patch("app.telegram_bot.handlers.series_menu_handler.get_series_details_by_name_llm", return_value=mock_series_result):
        calls = []
        async def mock_answer(self, text, **kwargs):
            calls.append(text)
        with patch.object(Message, "answer", new=mock_answer):
            await dp.feed_update(bot=bot, update=update)
        assert any("⬇️" in c for c in calls)

@pytest.mark.asyncio
async def test_top_10_series_e2e():
    bot, dp = create_bot_and_dispatcher()
    user = User(id=103, is_bot=False, first_name="Tester")
    chat = Chat(id=103, type="private")
    message = Message(
        message_id=4,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="🔥 Լավագույն 10 սերիալ"
    )
    update = Update(update_id=4, message=message)

    with patch("app.telegram_bot.handlers.series_menu_handler.get_top_10_series_llm", return_value=mock_series_result):
        calls = []
        async def mock_answer(self, text, **kwargs):
            calls.append(text)
        with patch.object(Message, "answer", new=mock_answer):
            await dp.feed_update(bot=bot, update=update)
        assert any("⬇️" in c for c in calls)
