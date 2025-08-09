import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.data import database as dbmod


import app.data.models.memory_model  # noqa: F401
import app.data.models.session_model  # noqa: F401


@pytest.fixture(scope="function")
def tmp_engine(tmp_path: Path):
    """Ժամանակավոր SQLite engine մեկ թեստի համար։"""
    test_db = tmp_path / "unit_memory.db"
    url = f"sqlite:///{test_db}"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    yield engine
    engine.dispose()
    if test_db.exists():
        os.remove(test_db)


@pytest.fixture(scope="function")
def patch_session_engine(monkeypatch, tmp_engine):
    """Patch անում ենք engine-ը և SessionLocal-ը դեպի temp engine։"""
    TestingSessionLocal = sessionmaker(
        bind=tmp_engine, autocommit=False, autoflush=False, expire_on_commit=False
    )
    monkeypatch.setattr(dbmod, "engine", tmp_engine, raising=True)
    monkeypatch.setattr(dbmod, "SessionLocal", TestingSessionLocal, raising=True)
    return tmp_engine


def test_init_db_creates_tables_with_patched_engine(patch_session_engine):
    insp = inspect(patch_session_engine)
    assert "user_memory" not in insp.get_table_names()
    assert "user_sessions" not in insp.get_table_names()

    dbmod.init_db()

    insp = inspect(patch_session_engine)
    tables = set(insp.get_table_names())
    assert {"user_memory", "user_sessions"} <= tables

    s = dbmod.SessionLocal()
    s.close()
