import pytest
from unittest.mock import AsyncMock, patch
from app.telegram_bot.handlers import mood_handler


class MockMessage:
    def __init__(self, text):
        self.text = text
        self.answer = AsyncMock()
        self.answer_photo = AsyncMock()


class MockFSMContext:
    def __init__(self):
        self._data = {}

    async def set_state(self, state):
        self._data["__state__"] = state

    async def update_data(self, **kwargs):
        self._data.update(kwargs)

    async def get_data(self):
        return self._data

    async def clear(self):
        self._data = {}


@pytest.mark.asyncio
async def test_mood_main_clears_state_and_replies():
    message = MockMessage("🧠 Mood Assistant")
    state = MockFSMContext()
    await mood_handler.mood_main(message, state)
    assert state._data == {}
    message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_mood_chosen_updates_state_and_replies():
    message = MockMessage("😢 Տխուր եմ")
    state = MockFSMContext()
    await mood_handler.mood_chosen(message, state)
    assert state._data["mood"] == "😢 Տխուր եմ"
    message.answer.assert_called_once()


@pytest.mark.asyncio
@patch(
    "app.telegram_bot.handlers.mood_handler.generate_songs_for_mood",
    return_value=[
        {
            "title": "Test Song",
            "artist": "Test Artist",
            "description": "Test Desc",
            "youtube": "https://youtu.be/test",
        }
    ],
)
async def test_mood_generate_songs(mock_gen):
    message = MockMessage("🎵 5 երգ")
    state = MockFSMContext()
    await state.update_data(mood="🤩 Ուրախ եմ")

    await mood_handler.mood_generate(message, state)
    assert "songs_for_download" in state._data
    assert message.answer.call_count >= 2


@pytest.mark.asyncio
@patch(
    "app.telegram_bot.handlers.mood_handler.generate_movies_for_mood",
    return_value=[
        {
            "title": "Test Movie",
            "genre": "Comedy",
            "director": "Someone",
            "trailer_url": "http://t",
            "watch_url": "http://w",
        }
    ],
)
async def test_mood_generate_movies(mock_gen):
    message = MockMessage("🎬 5 ֆիլմ")
    state = MockFSMContext()
    await state.update_data(mood="😤 Զայրացած եմ")

    await mood_handler.mood_generate(message, state)
    assert message.answer.call_count >= 2


@pytest.mark.asyncio
@patch(
    "app.telegram_bot.handlers.mood_handler.generate_quotes_for_mood",
    return_value="Quote 1\nQuote 2",
)
async def test_mood_generate_quotes(mock_gen):
    message = MockMessage("💬 5 մեջբերում")
    state = MockFSMContext()
    await state.update_data(mood="😴 Հոգնած եմ")

    await mood_handler.mood_generate(message, state)
    message.answer.assert_any_call("Quote 1\nQuote 2")


@pytest.mark.asyncio
@patch(
    "app.telegram_bot.handlers.mood_handler.generate_image_prompts_from_mood",
    return_value=["sunrise", "forest"],
)
@patch(
    "app.telegram_bot.handlers.mood_handler.generate_images_from_prompts",
    return_value=[("sunrise", "http://image1.jpg"), ("forest", "http://image2.jpg")],
)
async def test_mood_generate_images(mock_img_gen, mock_prompt_gen):
    message = MockMessage("🖼 2 նկարների նկարագրություն")
    state = MockFSMContext()
    await state.update_data(mood="💭 Խորհում եմ")

    await mood_handler.mood_generate(message, state)
    message.answer_photo.assert_called()


@pytest.mark.asyncio
async def test_show_mood_menu_clears_and_replies():
    message = MockMessage("❤️ Տրամադրությամբ երգեր")
    state = MockFSMContext()

    await mood_handler.show_mood_menu(message, state)
    assert state._data == {}
    message.answer.assert_called()


@pytest.mark.asyncio
async def test_back_to_mood_replies():
    message = MockMessage("🔙 Վերադառնալ տրամադրության ընտրությանը")
    await mood_handler.back_to_mood(message)
    message.answer.assert_called()


@pytest.mark.asyncio
async def test_back_to_main_menu_clears_state():
    message = MockMessage("🔝 Վերադառնալ գլխավոր մենյու")
    state = MockFSMContext()
    await state.update_data(mood="any")

    await mood_handler.back_to_main_menu(message, state)
    assert state._data == {}
    message.answer.assert_called()
