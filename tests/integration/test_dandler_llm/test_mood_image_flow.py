import pytest
from aiogram import Bot, Dispatcher
from aiogram.types import Message, User, Chat, Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from datetime import datetime

from app.telegram_bot.handlers.mood_handler import router
from app.llm import image_generator


@pytest.mark.asyncio
async def test_mood_image_flow(monkeypatch):
    # 🔁 Mock տվյալներ
    mock_prompts = ["Արևածագ լճի վրա", "Աղջիկը մենակ նստած է սրճարանում"]
    mock_images = [(mock_prompts[0], "https://test.image/1"), (mock_prompts[1], "https://test.image/2")]

    monkeypatch.setattr(image_generator, "generate_image_prompts_from_mood", lambda mood: mock_prompts)
    monkeypatch.setattr(image_generator, "generate_images_from_prompts", lambda prompts: mock_images)


    async def fake_answer(self, text, **kwargs):
        print(f"[Mocked answer]: {text}")

    monkeypatch.setattr(Message, "answer", fake_answer)
    
    async def fake_answer_photo(self, photo, **kwargs):
        print(f"[Mocked photo answer]: {photo}")

    monkeypatch.setattr(Message, "answer_photo", fake_answer_photo)

    #  Bot & Dispatcher
    storage = MemoryStorage()
    bot = Bot(token="123:ABC", default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    #  Ֆեյք user/chat
    user = User(id=123, is_bot=False, first_name="Մոչի", username="mochi")
    chat = Chat(id=456, type="private")

    #  Message
    message = Message(
        message_id=1,
        from_user=user,
        chat=chat,
        text="🖼 2 նկարների նկարագրություն",
        date=datetime.now(),
        message_thread_id=None
    )

    update = Update(update_id=99999, message=message)

    # 📡 Feed update properly
    await dp.feed_update(bot=bot, update=update)
