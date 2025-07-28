import pytest
from aiogram.types import ReplyKeyboardMarkup
from app.telegram_bot.menu import main_menu
from app.telegram_bot.bot import start_command_handler


class MockMessage:
    def __init__(self):
        self.text = "/start"
        self.response_text = None
        self.reply_markup = None

    async def answer(self, text, reply_markup=None):
        self.response_text = text
        self.reply_markup = reply_markup


@pytest.mark.asyncio
async def test_start_command_handler_response():
    message = MockMessage()
    await start_command_handler(message)

    expected_text_start = "👋 Բարի գալուստ SmartPromptBox Pro բոտ"
    assert message.response_text.startswith(expected_text_start), (
        f"Ստացված պատասխան:\n{message.response_text}"
    )

    assert isinstance(message.reply_markup, ReplyKeyboardMarkup), "reply_markup-ը պետք է լինի ReplyKeyboardMarkup"
    assert message.reply_markup.keyboard == main_menu.keyboard, "reply_markup keyboard-ը չի համընկնում main_menu-ի հետ"
