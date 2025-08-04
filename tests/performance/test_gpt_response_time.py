import pytest
import random
import os
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import User, Chat
from app.telegram_bot.handlers.gpt_memory_chat_handler import continue_conversation
from app.states.gpt_states import GPTMemoryStates  # ✅ Ավելացվել է FSM վիճակը

LOG_FILE = os.path.join(os.path.dirname(__file__), "slow_gpt_log.txt")


class FakeMessage:
    def __init__(self, text):
        self.message_id = 1
        self.from_user = User(id=random.randint(1000, 9999), is_bot=False, first_name="Tester")
        self.chat = Chat(id=self.from_user.id, type="private")
        self.date = datetime.now()
        self.text = text
        self.answer = AsyncMock()
        self.bot = MagicMock()
        self.bot.delete_message = AsyncMock()


class FakeFSMContext:
    def __init__(self):
        self._data = {}
        self._state = None

    async def set_state(self, state):
        self._state = state

    async def update_data(self, **kwargs):
        self._data.update(kwargs)

    async def clear(self):
        self._data.clear()
        self._state = None

    async def get_data(self):
        return self._data


@pytest.mark.asyncio
async def test_gpt_response_time():
    random_texts = [
        "Բարև, պատմիր ինձ մի բան",
        "Ի՞նչ ես մտածում GPT-ի մասին",
        "Ասա մի սյուրռեալ պատմություն",
        "Ինչպիսի՞ն կլինի ապագան քո կարծիքով",
        "Պատմիր ինձ մի հին լեգենդ",
        "Խոսա ինձ հետ իմ տրամադրության մասին",
        "Ինչո՞ւ են մարդիկ սիրում արվեստը",
        "Ասա մի փիլիսոփայական միտք",
        "Խոսիր ընկերության մասին",
        "Ուզում եմ մի փոքրիկ պատմվածք"
    ]

    text = random.choice(random_texts)
    message = FakeMessage(text=text)
    state = FakeFSMContext()
    await state.set_state(GPTMemoryStates.chatting) 

    start = datetime.now()
    await continue_conversation(message, state)
    end = datetime.now()

    duration = (end - start).total_seconds()
    print(f"⏱️ GPT response time: {duration:.3f} seconds")

    if duration > 15.0:
        status = "FAIL"
    elif duration > 4.0:
        status = "SLOW"
    else:
        status = "OK"

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {status} | {duration:.3f} sec | user_id={message.from_user.id} | Input: {message.text}\n")

    if status == "FAIL":
        pytest.fail(f"❌ GPT-ը պատասխանեց շատ դանդաղ՝ {duration:.3f} վայրկյան")
