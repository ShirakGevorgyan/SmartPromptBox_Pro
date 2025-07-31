import pytest
from unittest.mock import patch
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, User, Chat, Update
from datetime import datetime

from app.telegram_bot.handlers.mood_handler import router

mock_songs = [
    {
        "title": "Song 1",
        "artist": "Artist 1",
        "description": "Mood-based song 1",
        "youtube": "https://youtube.com/song1",
    }
]

mock_movies = [
    {
        "title": "Movie 1",
        "genre": "Drama",
        "director": "Director 1",
        "trailer_url": "https://youtube.com/trailer1",
        "watch_url": "https://imdb.com/movie1",
    }
]

mock_quotes = "1. Keep going!\n2. Never give up!\n3. Believe in yourself.\n4. Smile.\n5. Enjoy life."

mock_image_prompts = ["A sunny beach", "A cozy mountain cabin"]
mock_images = [
    ("A sunny beach", "https://example.com/image1.png"),
    ("A cozy mountain cabin", "https://example.com/image2.png"),
]


@pytest.mark.asyncio
async def test_mood_flow_e2e():
    bot = Bot(token="123456:TESTTOKEN", parse_mode="HTML")
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

        start_msg = Message(
            message_id=1,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🧠 Mood Assistant",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=1, message=start_msg))

        mood_msg = Message(
            message_id=2,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🤩 Ուրախ եմ",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=2, message=mood_msg))


        song_msg = Message(
            message_id=3,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🎵 5 երգ",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=3, message=song_msg))

        movie_msg = Message(
            message_id=4,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🎬 5 ֆիլմ",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=4, message=movie_msg))

        quote_msg = Message(
            message_id=5,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="💬 5 մեջբերում",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=5, message=quote_msg))


        image_msg = Message(
            message_id=6,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🖼 2 նկարների նկարագրություն",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=6, message=image_msg))

        back_msg = Message(
            message_id=7,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🔝 Վերադառնալ գլխավոր մենյու",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=7, message=back_msg))

    print("\n📤 Captured calls:")
    for c in calls:
        print("👉", c)

    assert any("տրամադրությունը" in c for c in calls)
    assert any("Գտնված 5 երգերը" in c for c in calls)
    assert any("ֆիլմ" in c or "Չհաջողվեց" in c for c in calls)
    assert any("մեջբերումներ" in c or "ներշնչող" in c for c in calls)
    assert any("Նկար 1" in c for c in calls)
    assert any("գլխավոր մենյու" in c.lower() for c in calls)
