import pytest
from unittest.mock import MagicMock, patch

from app.llm.series_picker import suggest_series_by_description_llm


@patch("app.llm.series_picker.client")
def test_suggest_series_llm_success(mock_client):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "🎥 Վերնագիր՝ Breaking Bad (2008)"
    mock_client.chat.completions.create.return_value = mock_response

    result = suggest_series_by_description_llm("դրամատիկ սերիալ")
    assert "🎥 Վերնագիր" in result
    assert "Breaking Bad" in result


@patch("app.llm.series_picker.client")
def test_suggest_series_llm_empty_response(mock_client):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = ""
    mock_client.chat.completions.create.return_value = mock_response

    result = suggest_series_by_description_llm("դրամատիկ սերիալ")
    assert result == ""


@patch("app.llm.series_picker.client")
def test_suggest_series_llm_exception(mock_client):
    mock_client.chat.completions.create.side_effect = Exception("GPT error")

    with pytest.raises(Exception) as exc_info:
        suggest_series_by_description_llm("դրամատիկ սերիալ")

    assert "GPT error" in str(exc_info.value)
