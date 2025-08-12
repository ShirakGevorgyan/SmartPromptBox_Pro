import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.data.models.memory_model import UserMemory
from app.llm import assistant


@pytest.mark.asyncio
@patch("app.llm.assistant.summarize_history", new_callable=AsyncMock)
@patch("app.llm.assistant.retry_async", new_callable=AsyncMock)
@patch("app.llm.assistant.save_history")
@patch("app.llm.assistant.load_history")
@patch("app.llm.assistant.SessionLocal")
async def test_gpt_assistant_conversation(
    mock_session_local,
    mock_load_history,
    mock_save_history,
    mock_retry_async,
    mock_summarize_history,
):
    mock_session = MagicMock()
    mock_session_local.return_value = mock_session
    mock_user = UserMemory(
        user_id="test_user",
        user_name=None,
        bot_name="Նարե",
        last_mood="neutral",
        history="[]",
    )
    mock_session.query().filter_by().first.return_value = mock_user

    mock_load_history.return_value = [
        {"role": "user", "content": "ես Մոչին եմ"},
        {"role": "assistant", "content": "Բարև"},
    ]

    mock_summarize_history.return_value = "Ամփոփում"
    mock_retry_async.return_value.choices = [
        MagicMock(message=MagicMock(content="Բարև Մոչի ջան 😊 Ինչով կարող եմ օգնել։"))
    ]
    mock_retry_async.return_value.usage = MagicMock(
        prompt_tokens=10, completion_tokens=20, total_tokens=30
    )

    result = await assistant.gpt_assistant_conversation("test_user", "Բարև")

    assert "Բարև" in result
    assert "Մոչի" in result
    assert mock_user.bot_name == "Նարե"
    assert "Մոչի" in mock_user.user_name
