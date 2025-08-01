import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models.base import Base
from app.llm.assistant import gpt_assistant_conversation, get_or_create_user, detect_user_mood, extract_names
from app.utils.summarizer import summarize_history


TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_get_or_create_user_creates_user(db_session):
    user_id = "mochi_123"
    user = get_or_create_user(db_session, user_id)
    assert user.user_id == user_id
    assert user.bot_name == "Նարե"
    assert user.last_mood == "neutral"


@pytest.mark.asyncio
async def test_detect_user_mood_positive():
    history = [{"role": "user", "content": "I feel great and happy today!"}]
    mood = detect_user_mood(history)
    assert mood == "positive"

@pytest.mark.asyncio
async def test_detect_user_mood_negative():
    history = [{"role": "user", "content": "I'm really sad and disappointed."}]
    mood = detect_user_mood(history)
    assert mood == "negative"


@pytest.mark.asyncio
async def test_summarize_history_summary_mocked():
    fake_history = [
        {"role": "user", "content": "Բարև"},
        {"role": "assistant", "content": "Բարև քեզ"},
        {"role": "user", "content": "Ի՞նչ ես կարողանում անել։"}
    ]
    with patch("app.utils.summarizer.get_openai_client") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.chat.completions.create.return_value = AsyncMock(
            choices=[AsyncMock(message=AsyncMock(content="Ամփոփ զրույց։"))]
        )
        mock_client.return_value = mock_instance

        result = await summarize_history(fake_history)
        assert "Ամփոփ" in result

@pytest.mark.asyncio
async def test_gpt_assistant_conversation(db_session):
    user_id = "mochi_456"
    message = "Բարև, ես Մոչին եմ։"

    with patch("app.llm.assistant.get_openai_client") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.chat.completions.create.return_value = AsyncMock(
            choices=[AsyncMock(message=AsyncMock(content="Բարև Մոչի ջան 😊"))],
            usage=AsyncMock(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        )
        mock_client.return_value = mock_instance

        with patch("app.llm.assistant.SessionLocal", return_value=db_session):
            result = await gpt_assistant_conversation(user_id, message)
            assert "Բարև" in result



@pytest.mark.asyncio
async def test_extract_names_missing():
    history = [
        {"role": "user", "content": "Բարև, ինչ կա չկա։"}
    ]
    user_name, bot_name = extract_names(history)
    assert user_name == ""
    assert bot_name == ""
