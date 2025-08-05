import pytest
from unittest.mock import patch, Mock, AsyncMock
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, User, Chat, Update
from datetime import datetime

from app.telegram_bot.handlers.random_songs_handler import router

@pytest.mark.asyncio
async def test_song_random_flow_e2e():
    bot = Bot(token="123456:TESTTOKEN", parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    user = User(id=123456, is_bot=False, first_name="Tester")
    chat = Chat(id=123456, type="private")
    captured = []

    async def mock_answer(self, text, **kwargs):
        captured.append(text)
        return Message(
            message_id=999,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text=text
        )

    with (
        patch.object(Message, "answer", new=mock_answer),
        patch("app.telegram_bot.handlers.random_songs_handler.generate_songs_random", new=Mock(return_value=[
            {
                "title": "Shape of You",
                "artist": "Ed Sheeran",
                "description": "Romantic Pop Song",
                "youtube": "https://youtube.com/example"
            }
        ])),
        patch("aiogram.client.bot.Bot.delete_message", new_callable=AsyncMock),
        patch("app.llm.song_llm.generate_songs_by_description", new=Mock(return_value=[])),
        patch("app.llm.song_llm.generate_top_songs_by_artist", new=Mock(return_value=[])),
        patch("app.llm.song_llm.generate_songs_by_genre", new=Mock(return_value=[])),
    ):
        start_msg = Message(
            message_id=1,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🔀 Պատահական երգ"
        )
        await dp.feed_update(bot=bot, update=Update(update_id=1, message=start_msg))

        back_msg = Message(
            message_id=2,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🔝 Վերադառնալ գլխավոր մենյու"
        )
        await dp.feed_update(bot=bot, update=Update(update_id=2, message=back_msg))

    print("\n📤 Captured messages:")
    for c in captured:
        print("👉", c)

    assert any("Սպասիր" in c for c in captured)
    assert any("Shape of You" in c for c in captured)
    assert any("🎼 Վերադարձ գլխավոր մենյու" in c for c in captured)
