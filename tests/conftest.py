import pytest
import warnings
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from unittest.mock import AsyncMock

warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture
def test_token():
    return "123:ABC"

@pytest.fixture
def memory_storage():
    return MemoryStorage()

@pytest.fixture
def fake_bot(test_token):
    bot = Bot(token=test_token)
    bot.send_message = AsyncMock()
    bot.delete_message = AsyncMock()
    return bot

@pytest.fixture
def bot_and_dispatcher(fake_bot, memory_storage):
    dp = Dispatcher(storage=memory_storage)
    return fake_bot, dp
