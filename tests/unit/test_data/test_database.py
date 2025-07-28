import os
import pytest
from sqlalchemy import inspect
from app.data import database
from app.data.models.base import Base

TEST_DB_PATH = "db/test_memory.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

@pytest.fixture(scope="module")
def test_engine():
    # Ստեղծում ենք թեստային engine
    engine = database.create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()

    # Ջնջում ենք ֆայլը թեստից հետո
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

@pytest.fixture(scope="function")
def session(test_engine):
    TestingSessionLocal = database.sessionmaker(bind=test_engine, expire_on_commit=False)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_init_db_creates_tables(test_engine):
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    
    assert "user_memory" in tables
    assert "user_sessions" in tables

