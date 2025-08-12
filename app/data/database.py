"""Database engine, session factory, and small utilities.

- Reads `DATABASE_URL` from the environment; falls back to local SQLite.
- Exposes a global `engine` and `SessionLocal`.
- `init_db()` ensures tables exist and (for SQLite) creates `./db/`.
- `get_db()` yields a session and guarantees it is closed afterwards.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models.base import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db/memory.db")

IS_SQLITE = DATABASE_URL.startswith("sqlite")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if IS_SQLITE else {},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def init_db() -> None:
    """Create the `db/` folder (for SQLite) and create tables if missing.

    Side effects:
        - For SQLite, ensures `./db/` exists.
        - Imports model modules so their tables are registered on `Base.metadata`.
        - Calls `Base.metadata.create_all(bind=engine)`.

    This function is idempotent and safe to call multiple times.
    """
    if IS_SQLITE:
        Path("db").mkdir(parents=True, exist_ok=True)

    from app.data.models import session_model  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a database session and close it when the caller is done.

    Yields:
        sqlalchemy.orm.Session: an open session bound to the global engine.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
