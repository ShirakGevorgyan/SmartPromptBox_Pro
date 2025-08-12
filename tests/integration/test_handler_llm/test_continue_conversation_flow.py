import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from app.states.gpt_states import GPTMemoryStates
from app.telegram_bot.handlers.gpt_memory_chat_handler import continue_conversation


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.gpt_memory_chat_handler.gpt_assistant_conversation")
@patch("app.telegram_bot.handlers.gpt_memory_chat_handler.get_or_create_user_session")
@patch("app.telegram_bot.handlers.gpt_memory_chat_handler.update_session_info")
@patch("app.telegram_bot.handlers.gpt_memory_chat_handler.SessionLocal")
async def test_continue_conversation_flow(
    mock_session_local,
    mock_update_session_info,
    mock_get_or_create_user_session,
    mock_gpt_assistant_conversation,
):
    mock_gpt_assistant_conversation.return_value = "Սա մոկված պատասխան է"

    mock_session = MagicMock()
    mock_session_local.return_value = mock_session
    mock_get_or_create_user_session.return_value = MagicMock()
    mock_update_session_info.return_value = None

    storage = MemoryStorage()
    state = FSMContext(storage=storage, key=("TelegramBot", 123456))
    await state.set_state(GPTMemoryStates.chatting)
    await state.update_data(chat_history=[], message_ids=[])

    message = AsyncMock(spec=Message)
    message.text = "Բարև, ես Մոչին եմ"
    message.chat = MagicMock(id=123456)
    message.from_user = MagicMock(id=123456)
    message.bot.delete_message = AsyncMock()
    message.answer = AsyncMock(return_value=MagicMock(message_id=42))

    await continue_conversation(message, state)

    data = await state.get_data()
    print("\nCHATHISTORY:", data["chat_history"])
    assert "chat_history" in data
    assert len(data["chat_history"]) == 2
    assert data["chat_history"][0]["role"] == "user"
    assert data["chat_history"][1]["role"] == "assistant"
