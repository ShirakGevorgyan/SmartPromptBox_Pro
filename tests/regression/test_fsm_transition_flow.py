import pytest
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from app.telegram_bot.handlers.series_menu_handler import router, SeriesStates


@pytest.mark.asyncio
async def test_series_description_state_transition():

    storage = MemoryStorage()
    bot = Bot(token="123:ABC", parse_mode=None)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    user_id = 42
    chat_id = 42

    ctx: FSMContext = dp.fsm.get_context(bot, chat_id, user_id)

    await ctx.set_state(SeriesStates.waiting_for_description)

    current_state = await ctx.get_state()
    assert current_state == SeriesStates.waiting_for_description.state
