from aiogram.fsm.state import StatesGroup, State


class GPTMemoryStates(StatesGroup):
    chatting = State()
