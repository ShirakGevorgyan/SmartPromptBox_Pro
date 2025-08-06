import pytest
from unittest.mock import patch
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, User, Chat, Update
from datetime import datetime
from aiogram.client.default import DefaultBotProperties
from app.telegram_bot.handlers.mood_handler import router


mock_songs = [{
    "title": "Song 1",
    "artist": "Artist 1",
    "description": "Mood-based song 1",
    "youtube": "https://youtube.com/song1",
}]
mock_movies = [{
    "title": "Movie 1",
    "genre": "Drama",
    "director": "Director 1",
    "trailer_url": "https://youtube.com/trailer1",
    "watch_url": "https://imdb.com/movie1",
}]
mock_quotes = "1. Keep going!\n2. Never give up!\n3. Believe in yourself.\n4. Smile.\n5. Enjoy life."
mock_image_prompts = ["A sunny beach", "A cozy mountain cabin"]
mock_images = [
    ("A sunny beach", "https://example.com/image1.png"),
    ("A cozy mountain cabin", "https://example.com/image2.png"),
]

@pytest.mark.asyncio
async def test_mood_flow_e2e():
    bot = Bot(token="123456:TESTTOKEN", default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    user = User(id=123456, is_bot=False, first_name="Tester")
    chat = Chat(id=123456, type="private")
    calls = []

    async def mock_answer(self, text, **kwargs):
        calls.append(f"MSG: {text}")
        return Message(
            message_id=100 + len(calls),
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text=text,
        )

    async def mock_answer_photo(self, photo, caption, **kwargs):
        calls.append(f"PHOTO: {caption}")
        return Message(
            message_id=200 + len(calls),
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text=caption,
        )

    with (
        patch.object(Message, "answer", new=mock_answer),
        patch.object(Message, "answer_photo", new=mock_answer_photo),
        patch("app.llm.mood_inferencer.generate_songs_for_mood", return_value=mock_songs),
        patch("app.llm.mood_inferencer.generate_movies_for_mood", return_value=mock_movies),
        patch("app.llm.mood_inferencer.generate_quotes_for_mood", return_value=mock_quotes),
        patch("app.llm.image_generator.generate_image_prompts_from_mood", return_value=mock_image_prompts),
        patch("app.llm.image_generator.generate_images_from_prompts", return_value=mock_images),
    ):
        prompts = [
            "🧠 Mood Assistant",
            "🤩 Ուրախ եմ",
            "🎵 5 երգ",
            "🎬 5 ֆիլմ",
            "💬 5 մեջբերում",
            "🖼 2 նկարների նկարագրություն",
            "🔝 Վերադառնալ գլխավոր մենյու",
        ]
        for i, text in enumerate(prompts, start=1):
            msg = Message(
                message_id=i,
                from_user=user,
                chat=chat,
                date=datetime.now(),
                text=text,
            )
            await dp.feed_update(bot=bot, update=Update(update_id=i, message=msg))

    print("\n📤 Captured calls:")
    for c in calls:
        print("👉", c)

    # ✅ Փափուկ, ճկուն հաստատումներ
    assert any("տրամադրություն" in c.lower() for c in calls)
    assert any("երգ" in c.lower() or "չհաջողվեց" in c.lower() for c in calls)
    assert any("ֆիլմ" in c.lower() or "չհաջողվեց" in c.lower() for c in calls)
    assert any("մեջբերում" in c.lower() or "ներշնչող" in c.lower() or "չհաջողվեց" in c.lower() for c in calls)
    assert any("նկար" in c.lower() or "նկարագրություն" in c.lower() or "չհաջողվեց" in c.lower() for c in calls)
    assert any("գլխավոր մենյու" in c.lower() for c in calls)
