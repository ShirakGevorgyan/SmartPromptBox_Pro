

import pytest
from unittest.mock import patch, AsyncMock
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, User, Chat, Update
from datetime import datetime
from app.telegram_bot.handlers.random_songs_handler import router

@pytest.mark.asyncio
async def test_gpt_conversation_e2e():
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
        patch("app.llm.assistant.gpt_assistant_conversation", new=AsyncMock(return_value="Ես GPT մոդել եմ 😊")),
        patch("app.data.db_session_tracker.get_or_create_user_session", return_value=None),
        patch("app.data.db_session_tracker.update_session_info", return_value=None),
        patch("aiogram.client.bot.Bot.delete_message", new_callable=AsyncMock)
    ):
        # 1. Սկսում ենք GPT զրույցը
        start_msg = Message(
            message_id=1,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="⭐️ Խոսիր ինձ հետ"
        )
        await dp.feed_update(bot=bot, update=Update(update_id=1, message=start_msg))

        # 2. Ուղարկում ենք GPT հարց
        gpt_msg = Message(
            message_id=2,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="Ո՞վ ես դու"
        )
        await dp.feed_update(bot=bot, update=Update(update_id=2, message=gpt_msg))

        # 3. Վերադարձ գլխավոր մենյու
        back_msg = Message(
            message_id=3,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🔝 Վերադառնալ գլխավոր մենյու"
        )
        await dp.feed_update(bot=bot, update=Update(update_id=3, message=back_msg))

        # 4. Կրկին սկսում ենք զրույց, ապա մաքրում
        restart_msg = Message(
            message_id=4,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="⭐️ Խոսիր ինձ հետ"
        )
        await dp.feed_update(bot=bot, update=Update(update_id=4, message=restart_msg))

        clear_msg = Message(
            message_id=5,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🧹 Մաքրել զրույցը"
        )
        await dp.feed_update(bot=bot, update=Update(update_id=5, message=clear_msg))

    print("\n📤 Captured messages:")
    for c in captured:
        print("👉", c)

    assert any("🧠" in c for c in captured)  # սկիզբ
    assert any("Ես GPT մոդել" in c for c in captured)  # GPT պատասխանը
    assert any("🏠" in c for c in captured)  # գլխավոր մենյու
    assert any("📭 Զրույցը մաքրված է" in c for c in captured)  # մաքրում
