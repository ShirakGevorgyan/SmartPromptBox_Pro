import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import User, Chat
from app.telegram_bot.handlers.gpt_memory_chat_handler import continue_conversation


class FakeMessage:
    def __init__(self, text):
        self.message_id = 1
        self.from_user = User(id=1, is_bot=False, first_name="Tester")
        self.chat = Chat(id=1, type="private")
        self.date = datetime.now()
        self.text = text
        self.answer = AsyncMock()
        self.bot = MagicMock()
        self.bot.delete_message = AsyncMock()


class FakeFSMContext:
    def __init__(self):
        self._data = {}

    async def set_state(self, state): pass
    async def update_data(self, **kwargs): self._data.update(kwargs)
    async def clear(self): self._data.clear()
    async def get_data(self): return self._data


@pytest.mark.parametrize("malicious_input", [
    "<script>alert('XSS')</script>",
    "'; DROP TABLE users; --",
    "🔥" * 1000,
    "SELECT * FROM users WHERE username = 'admin'",
    "`rm -rf /`",
])
@pytest.mark.asyncio
async def test_continue_conversation_sanitization(malicious_input):
    message = FakeMessage(text=malicious_input)
    state = FakeFSMContext()

    try:
        await continue_conversation(message, state)
    except Exception as e:
        pytest.fail(f"Bot crashed on malicious input: {malicious_input}\nError: {str(e)}")

    message.answer.assert_called()
