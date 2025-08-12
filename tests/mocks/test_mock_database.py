import pytest
from unittest.mock import MagicMock

from app.data.memory_service import load_history, save_history
from app.data.models.memory_model import UserMemory


def test_load_history_returns_correct_structure():
    mock_session = MagicMock()

    mock_session.query().filter_by().order_by().all.return_value = [
        UserMemory(user_id="123", role="user", content="Hello"),
        UserMemory(user_id="123", role="assistant", content="Hi there!"),
    ]

    result = load_history(mock_session, user_id="123")

    assert isinstance(result, list)
    assert result == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]


def test_save_history_deletes_and_inserts():
    mock_session = MagicMock()

    history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello"},
    ]

    save_history(mock_session, user_id="123", history=history)

    mock_session.query().filter_by().delete.assert_called_once()
    assert mock_session.add.call_count == 2
    assert mock_session.commit.call_count == 2


def test_save_history_handles_empty_history():
    mock_session = MagicMock()
    history = []

    save_history(mock_session, user_id="123", history=history)

    mock_session.query().filter_by().delete.assert_called_once()
    mock_session.add.assert_not_called()
    assert mock_session.commit.call_count == 2


def test_save_history_db_error_handling():
    mock_session = MagicMock()
    mock_session.query().filter_by().delete.side_effect = Exception("DB Error")

    history = [{"role": "user", "content": "Test"}]

    with pytest.raises(Exception) as exc_info:
        save_history(mock_session, user_id="123", history=history)

    assert "DB Error" in str(exc_info.value)
