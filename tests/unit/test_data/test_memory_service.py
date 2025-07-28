import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models.base import Base
from app.data.memory_service import load_history, save_history


# 🔧 Test-ի engine ու session
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


def test_save_and_load_history(test_session):
    user_id = "test_user_123"
    test_history = [
        {"role": "user", "content": "Բարև"},
        {"role": "assistant", "content": "Բարև Մոչի ջան"},
    ]

    # 💾 Պահպանում ենք պատմությունը
    save_history(test_session, user_id, test_history)

    # 📤 Բեռնում ենք պատմությունը
    loaded_history = load_history(test_session, user_id)

    assert loaded_history == test_history
    assert len(loaded_history) == 2
    assert loaded_history[0]["role"] == "user"
    assert loaded_history[1]["content"] == "Բարև Մոչի ջան"
