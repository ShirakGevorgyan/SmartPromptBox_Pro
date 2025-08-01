import pytest
from unittest.mock import patch, AsyncMock
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, User, Chat, Update
from datetime import datetime

from app.telegram_bot.handlers.gpt_memory_chat_handler import router


@pytest.mark.asyncio
async def test_gpt_memory_chat_e2e():
    bot = Bot(token="123456:TESTTOKEN", parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    user = User(id=123456, is_bot=False, first_name="Tester")
    chat = Chat(id=123456, type="private")

    start_msg = Message(
        message_id=1,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="⭐️ Խոսիր ինձ հետ"
    )
    start_update = Update(update_id=1001, message=start_msg)


    gpt_msg = Message(
        message_id=2,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text="Ո՞վ ես դու"
    )
    gpt_update = Update(update_id=1002, message=gpt_msg)

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
        patch("app.llm.assistant.gpt_assistant_conversation", new=AsyncMock(return_value="Ես GPT մոդել եմ 😊")),
        patch("app.data.db_session_tracker.get_or_create_user_session", return_value=None),
        patch("app.data.db_session_tracker.update_session_info", return_value=None)
    ):

        await dp.feed_update(bot=bot, update=start_update)

        await dp.feed_update(bot=bot, update=gpt_update)

    print("\n📤 Captured messages:")
    for c in captured:
        print(c)

    assert any("🧠" in c or "🤖" in c or "Ես GPT մոդել" in c for c in captured)
