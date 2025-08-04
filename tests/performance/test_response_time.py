import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from aiogram.types import User, Chat
from app.telegram_bot.bot import start_command_handler


class FakeMessage:
    def __init__(self, text="/start"):
        self.message_id = 1
        self.from_user = User(id=1, is_bot=False, first_name="Tester")
        self.chat = Chat(id=1, type="private")
        self.date = datetime.now()
        self.text = text
        self.answer = AsyncMock()


@pytest.mark.asyncio
async def test_start_response_time():
    message = FakeMessage()

    start_time = datetime.now()
    await start_command_handler(message)
    end_time = datetime.now()

    duration = (end_time - start_time).total_seconds()

    print(f"⏱️ Bot response time: {duration:.3f} seconds")

    assert duration < 1.0, f"❌ Պատասխանը շատ դանդաղ է: {duration:.3f} վայրկյան"
