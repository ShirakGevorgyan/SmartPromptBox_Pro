import pytest
from unittest.mock import patch
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, User, Chat, Update
from datetime import datetime
from aiogram.client.default import DefaultBotProperties
from app.telegram_bot.handlers.img_handler import router


@pytest.mark.asyncio
async def test_img_generation_e2e(tmp_path):
    bot = Bot(
    token="123456:TESTTOKEN",
    default=DefaultBotProperties(parse_mode="HTML")
)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    user = User(id=123456, is_bot=False, first_name="Tester")
    chat = Chat(id=123456, type="private")

    captured = []

    async def mock_answer(self, text, **kwargs):
        captured.append(f"MSG: {text}")
        return Message(
            message_id=123,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text=text,
        )

    async def mock_answer_photo(self, photo, caption, **kwargs):
        captured.append(f"PHOTO: {caption}")
        return Message(
            message_id=124,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text=caption,
        )

    fake_img_path = tmp_path / "generated_image.png"
    fake_img_path.write_bytes(b"fakeimagecontent")

    with (
        patch.object(Message, "answer", new=mock_answer),
        patch.object(Message, "answer_photo", new=mock_answer_photo),
        # ✅ Ահա ճիշտ patch-ը՝ img_handler-ի մեջ է օգտագործվում
        patch("app.telegram_bot.handlers.img_handler.generate_image", return_value=str(fake_img_path)),
    ):
        start_msg = Message(
            message_id=1,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🎨 Նկար գեներացիա",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=1, message=start_msg))

        prompt_msg = Message(
            message_id=2,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="լուսին սարերի վրա",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=2, message=prompt_msg))

        back_msg = Message(
            message_id=3,
            from_user=user,
            chat=chat,
            date=datetime.now(),
            text="🏠 Վերադառնալ գլխավոր մենյու",
        )
        await dp.feed_update(bot=bot, update=Update(update_id=3, message=back_msg))

    print("\n📤 Captured messages:")
    for c in captured:
        print("👉", c)

    assert any("Տուր նկարագրություն" in c for c in captured)
    assert any("ստեղծում եմ" in c.lower() for c in captured)
    assert any("Ահա քո նկարը" in c for c in captured)
    assert any("գլխավոր մենյու" in c.lower() for c in captured)
