import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from aiogram.types import User, Chat
from app.telegram_bot.bot import start_command_handler
from app.telegram_bot.menu import main_menu


class FakeMessage:
    def __init__(self, text="/start"):
        self.message_id = 1
        self.from_user = User(id=1, is_bot=False, first_name="Tester")
        self.chat = Chat(id=1, type="private")
        self.date = datetime.now()
        self.text = text
        self.answer = AsyncMock()

@pytest.mark.asyncio
async def test_start_command_handler():
    message = FakeMessage()
    await start_command_handler(message)

    message.answer.assert_called_once()
    args, kwargs = message.answer.call_args

    assert "Բարի գալուստ SmartPromptBox Pro բոտ" in args[0]
    assert kwargs["reply_markup"] == main_menu
