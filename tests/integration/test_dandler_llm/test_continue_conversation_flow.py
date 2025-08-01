import warnings
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.telegram_bot.handlers.gpt_memory_chat_handler import continue_conversation
from app.states.gpt_states import GPTMemoryStates
from app.data.database import SessionLocal
from app.data.models.memory_model import UserMemory


@pytest.mark.asyncio
@patch("app.llm.assistant.retry_async")
async def test_continue_conversation_flow(mock_retry_async):
    # ✅ Մոկված GPT պատասխանը
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Սա մոկված պատասխան է"))
    ]
    mock_response.usage = MagicMock(
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15
    )
    mock_retry_async.return_value = mock_response


    storage = MemoryStorage()
    state = FSMContext(storage=storage, key=("TelegramBot", 123456))

    test_input = "Բարև, ես Մոչին եմ"

    message = AsyncMock(spec=Message)
    message.text = test_input
    message.chat = MagicMock(id=123456)
    message.from_user = MagicMock(id=123456)
    message.bot.delete_message = AsyncMock()
    message.answer = AsyncMock(return_value=MagicMock(message_id=999))

    await state.set_state(GPTMemoryStates.chatting)
    await state.update_data(chat_history=[], message_ids=[])

    await continue_conversation(message, state)

    data = await state.get_data()
    assert "chat_history" in data
    assert len(data["chat_history"]) >= 2
    assert data["chat_history"][-1]["role"] == "assistant"
    assert "Սա մոկված պատասխան է" in data["chat_history"][-1]["content"]


    db = SessionLocal()
    rows = db.query(UserMemory).filter_by(user_id="123456").all()
    assert len(rows) >= 2
    assert rows[-1].role == "assistant"
    assert "Սա մոկված պատասխան է" in rows[-1].content
    db.close()

warnings.filterwarnings("ignore", category=DeprecationWarning)
