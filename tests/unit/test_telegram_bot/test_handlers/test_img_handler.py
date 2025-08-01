import pytest
from unittest.mock import AsyncMock, patch

from app.telegram_bot.handlers import img_handler
from app.telegram_bot.handlers.img_handler import ImageStates


class MockMessage:
    def __init__(self, text=""):
        self.text = text
        self.chat = type("Chat", (), {"id": 123})
        self.from_user = type("FromUser", (), {"id": 456})
        self.bot = AsyncMock()

    async def answer(self, text, reply_markup=None):
        return AsyncMock()

    async def answer_photo(self, photo, caption=None):
        return AsyncMock()


class MockFSMContext:
    def __init__(self):
        self._data = {}

    async def set_state(self, state):
        self._data["__state__"] = state

    async def clear(self):
        self._data.clear()

    async def update_data(self, **kwargs):
        self._data.update(kwargs)

    async def get_data(self):
        return self._data


@pytest.mark.asyncio
async def test_ask_for_prompt_sets_state():
    message = MockMessage("🎨 Նկար գեներացիա")
    state = MockFSMContext()

    await img_handler.ask_for_prompt(message, state)

    assert state._data["__state__"] == ImageStates.waiting_for_prompt


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.img_handler.generate_image", return_value="test_image.png")
@patch("os.path.exists", return_value=True)
@patch("os.remove")
async def test_handle_prompt_success(mock_remove, mock_exists, mock_generate):
    message = MockMessage("Գեներացիա արա՝ մի շունով նկար")
    state = MockFSMContext()

    await img_handler.handle_prompt(message, state)

    assert "__state__" not in state._data  


@pytest.mark.asyncio
@patch("app.telegram_bot.handlers.img_handler.generate_image", return_value=None)
@patch("os.path.exists", return_value=False)
async def test_handle_prompt_failure(mock_exists, mock_generate):
    message = MockMessage("Նկար չստացվեց")
    state = MockFSMContext()

    await img_handler.handle_prompt(message, state)

    assert "__state__" not in state._data 


@pytest.mark.asyncio
async def test_go_to_main_menu_clears_state():
    message = MockMessage("🏠 Վերադառնալ գլխավոր մենյու")
    state = MockFSMContext()

    await img_handler.go_to_main_menu(message, state)

    assert state._data == {}
