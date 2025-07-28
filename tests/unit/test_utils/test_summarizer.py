import pytest
from unittest.mock import AsyncMock, patch
from app.utils.summarizer import summarize_history

@pytest.mark.asyncio
@patch("app.utils.summarizer.get_openai_client")
async def test_summarize_history(mock_get_client):
    # Arrange: mock OpenAI response
    mock_response = AsyncMock()
    mock_response.chat.completions.create.return_value = AsyncMock(
        choices=[AsyncMock(message=AsyncMock(content="📝 This is a summary."))]
    )
    mock_get_client.return_value = mock_response

    history = [
        {"role": "user", "content": "Ողջույն"},
        {"role": "assistant", "content": "Բարև, ինչպես կարող եմ օգնել քեզ"},
        {"role": "user", "content": "Ասա ինձ մի բան Արիստոտելի մասին"},
        {"role": "assistant", "content": "Արիստոտելը հին հույն փիլիսոփա է։"},
    ]

    # Act
    result = await summarize_history(history)

    # Assert
    assert isinstance(result, str)
    assert "summary" in result.lower() or "📝" in result
