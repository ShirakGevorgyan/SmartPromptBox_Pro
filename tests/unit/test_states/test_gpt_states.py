from app.states.gpt_states import GPTMemoryStates
from aiogram.fsm.state import State

def test_gptmemorystates_contains_chatting_state():
    assert hasattr(GPTMemoryStates, "chatting")
    assert isinstance(GPTMemoryStates.chatting, State)
