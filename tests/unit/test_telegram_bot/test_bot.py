import re
import pytest
from aiogram.types import ReplyKeyboardMarkup

from app.telegram_bot.menu import main_menu
from app.telegram_bot.bot import start_command_handler


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "")


class MockMessage:
    def __init__(self):
        self.text = "/start"
        self.response_text = None
        self.reply_markup = None

    async def answer(self, text, reply_markup=None, **kwargs):
        self.response_text = text
        self.reply_markup = reply_markup


@pytest.mark.asyncio
async def test_start_command_handler_response():
    message = MockMessage()
    await start_command_handler(message)

    plain = strip_html(message.response_text).strip()

    assert plain.startswith("👋 Բարի գալուստ"), f"Welcome prefix not found:\n{plain}"

    assert "SmartPromptBox Pro" in plain, f"Project name missing:\n{plain}"

    help_variants = ("Օգնություն", "/help")
    assert any(v in plain for v in help_variants), f"Help hint missing:\n{plain}"

    for fragment in ["Mood", "Ֆիլմեր", "Սերիալներ", "Երգեր", "Նկար"]:
        assert fragment in plain, f"Fragment '{fragment}' not found in:\n{plain}"

    assert isinstance(
        message.reply_markup, ReplyKeyboardMarkup
    ), "reply_markup must be ReplyKeyboardMarkup"
    assert (
        message.reply_markup.keyboard == main_menu.keyboard
    ), "main menu keyboard mismatch"
