import pytest
from unittest.mock import patch
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, User, Chat, Update
from datetime import datetime
import copy

from app.telegram_bot.handlers.movie_menu_handler import router as movie_router_original, FilmStates

mock_movie_result = """
🎥 Վերնագիր (2020)
🎭 Ժանրը՝ Դրամա
🎬 Ռեժիսոր՝ John Doe
🎭 Դերասաններ՝ Jane, Mike, Bob
📜 Սյուժե՝ Something deep.
📊 IMDb գնահատական՝ 8.5
▶️ Տրեյլեր՝ [Դիտել](https://youtube.com/trailer)
🎞️ Դիտելու հղում՝ [IMDB](https://imdb.com/watch)
"""

def create_bot_and_dispatcher():
    movie_router = copy.deepcopy(movie_router_original)
    bot = Bot(token="123456:TESTTOKEN", parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(movie_router)
    return bot, dp

@pytest.mark.asyncio
async def test_random_movie_e2e():
    bot, dp = create_bot_and_dispatcher()
    user = User(id=123, is_bot=False, first_name="Tester")
    chat = Chat(id=123, type="private")
    message = Message(
        message_id=1,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="🎲 Պատահական ֆիլմ"
    )
    update = Update(update_id=123, message=message)

    with patch("app.llm.movie_picker.get_random_movie_llm", return_value=mock_movie_result):
        calls = []

        async def mock_answer(self, text, **kwargs):
            calls.append(text)

        with patch.object(Message, "answer", new=mock_answer):
            await dp.feed_update(bot=bot, update=update)

        assert any("⬇️ Ընտրիր հաջորդ քայլը։" in c or "🎯 Ընտրում եմ" in c for c in calls)


@pytest.mark.asyncio
async def test_movie_by_description_e2e():
    bot, dp = create_bot_and_dispatcher()
    user = User(id=789, is_bot=False, first_name="Tester")
    chat = Chat(id=789, type="private")

    context = dp.fsm.get_context(bot=bot, user_id=user.id, chat_id=chat.id)
    await context.set_state(FilmStates.waiting_for_description)

    message = Message(
        message_id=2,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="I want something emotional"
    )
    update = Update(update_id=456, message=message)

    with patch("app.llm.movie_picker.suggest_movies_by_description_llm", return_value=mock_movie_result):
        calls = []

        async def mock_answer(self, text, **kwargs):
            calls.append(text)

        with patch.object(Message, "answer", new=mock_answer):
            await dp.feed_update(bot=bot, update=update)

        assert any("⬇️ Ընտրիր հաջորդ քայլը։" in c for c in calls)


@pytest.mark.asyncio
async def test_movie_by_name_e2e():
    bot, dp = create_bot_and_dispatcher()
    user = User(id=456, is_bot=False, first_name="Tester")
    chat = Chat(id=456, type="private")

    context = dp.fsm.get_context(bot=bot, user_id=user.id, chat_id=chat.id)
    await context.set_state(FilmStates.waiting_for_movie_name)

    message = Message(
        message_id=3,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="Inception"
    )
    update = Update(update_id=789, message=message)

    with patch("app.llm.movie_picker.get_movie_details_by_name_llm", return_value=mock_movie_result):
        calls = []

        async def mock_answer(self, text, **kwargs):
            calls.append(text)

        with patch.object(Message, "answer", new=mock_answer):
            await dp.feed_update(bot=bot, update=update)

        assert any("⬇️ Ընտրիր հաջորդ քայլը։" in c for c in calls)


@pytest.mark.asyncio
async def test_top_10_movies_e2e():
    bot, dp = create_bot_and_dispatcher()
    user = User(id=321, is_bot=False, first_name="Tester")
    chat = Chat(id=321, type="private")

    message = Message(
        message_id=4,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="🔥 Լավագույն 10 ֆիլմ"
    )
    update = Update(update_id=888, message=message)

    with patch("app.llm.movie_picker.get_top_10_movies_llm", return_value=mock_movie_result):
        calls = []

        async def mock_answer(self, text, **kwargs):
            calls.append(text)

        with patch.object(Message, "answer", new=mock_answer):
            await dp.feed_update(bot=bot, update=update)

        assert any("⬇️ Ընտրիր հաջորդ քայլը։" in c for c in calls)


@pytest.mark.asyncio
async def test_movie_by_genre_e2e():
    bot, dp = create_bot_and_dispatcher()
    user = User(id=111, is_bot=False, first_name="Tester")
    chat = Chat(id=111, type="private")

    context = dp.fsm.get_context(bot=bot, user_id=user.id, chat_id=chat.id)
    await context.set_state(FilmStates.waiting_for_genre)

    message = Message(
        message_id=5,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="🎭 Դրամա"
    )
    update = Update(update_id=999, message=message)

    with patch("app.llm.movie_picker.get_movies_by_genre_llm", return_value=mock_movie_result):
        calls = []

        async def mock_answer(self, text, **kwargs):
            calls.append(text)

        with patch.object(Message, "answer", new=mock_answer):
            await dp.feed_update(bot=bot, update=update)

        assert any("⬇️" in c or "Կրկին ընտրի" in c for c in calls)
