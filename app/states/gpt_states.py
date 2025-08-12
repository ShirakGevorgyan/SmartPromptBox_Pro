"""Finite State Machine (FSM) states for GPT memory chat."""

from aiogram.fsm.state import StatesGroup, State


class GPTMemoryStates(StatesGroup):
    """Conversation states for the memory-enabled GPT chat flow."""

    chatting = State()
