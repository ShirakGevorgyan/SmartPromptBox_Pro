import pytest
from unittest.mock import AsyncMock, patch
from app.telegram_bot.handlers import gpt_memory_chat_handler


class MockMessage:
    def __init__(self, text, chat_id=123, user_id=456):
        self.text = text
        self.chat = type("Chat", (), {"id": chat_id})
        self.from_user = type("User", (), {"id": user_id})
        self.message_id = 111
        self.bot = AsyncMock()

    async def answer(self, text, reply_markup=None):
        msg = MockMessage(text)
        msg.message_id = 222
        return msg


class MockFSMContext:
    def __init__(self):
        self.state = None
        self.data = {}

    async def set_state(self, state):
        self.state = state

    async def update_data(self, **kwargs):
        self.data.update(kwargs)

    async def get_data(self):
        return self.data

    async def clear(self):
        self.state = None
        self.data.clear()


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.gpt_memory_chat_handler.gpt_assistant_conversation", new_callable=AsyncMock)
@patch("app.telegram_bot.handlers.gpt_memory_chat_handler.get_or_create_user_session")
@patch("app.telegram_bot.handlers.gpt_memory_chat_handler.update_session_info")
async def test_normal_conversation_flow(mock_update, mock_create, mock_gpt):
    mock_gpt.return_value = "GPT Պատասխան"

    message = MockMessage("Ո՞րն է կյանքի իմաստը")
    state = MockFSMContext()
    state.data = {"chat_history": [], "message_ids": []}

    await gpt_memory_chat_handler.continue_conversation(message, state)

    assert len(state.data["chat_history"]) == 2
    assert state.data["chat_history"][-1]["role"] == "assistant"
    assert state.data["chat_history"][-1]["content"] == "GPT Պատասխան"
