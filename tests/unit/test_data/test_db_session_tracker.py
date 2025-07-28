import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from app.data.models.base import Base
from app.data.models.session_model import UserSession
from app.data.db_session_tracker import (
    get_or_create_user_session,
    update_session_info,
    get_session_info,
)

# 🔧 SQLite in-memory session setup
@pytest.fixture(scope="function")
def test_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_get_or_create_user_session(test_session):
    user_id = "user123"
    session_id = get_or_create_user_session(test_session, user_id)
    
    assert isinstance(session_id, str)
    assert len(session_id) > 0

    # նույն user_id-ով կրկին կանչելու դեպքում պետք է վերադարձնի նույն session_id (միջակայքը թույլ է տալիս)
    same_session_id = get_or_create_user_session(test_session, user_id)
    assert session_id == same_session_id


def test_update_and_get_session_info(test_session):
    user_id = "user456"

    # Նախ session ստեղծել
    get_or_create_user_session(test_session, user_id)

    # Ավելացնել ինֆո
    update_session_info(
        db=test_session,
        user_id=user_id,
        topic="Music",
        last_question="Ով է երգում This is the life երգը?"
    )

    topic, question = get_session_info(test_session, user_id)
    assert topic == "Music"
    assert "This is the life" in question


def test_session_timeout_creates_new_session(test_session):
    user_id = "user789"
    original_session_id = get_or_create_user_session(test_session, user_id)

    # Հինացնում ենք session-ը
    session = test_session.query(UserSession).filter_by(user_id=user_id).first()
    session.last_seen = datetime.utcnow() - timedelta(seconds=4000)  # > SESSION_TIMEOUT
    test_session.commit()

    new_session_id = get_or_create_user_session(test_session, user_id)

    assert new_session_id != original_session_id
