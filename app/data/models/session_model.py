"""SQLAlchemy model for lightweight per-user session tracking.

Used to keep short-lived session IDs and auxiliary fields like topic and the
last question, plus a `last_seen` timestamp to expire stale sessions.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.data.models.base import Base


class UserSession(Base):
    """Per-user session row.

    Attributes:
        user_id: Telegram user identifier.
        session_id: Unique random session key.
        topic: Optional last topic/category.
        last_question: Optional text of the last user question.
        last_seen: UTC timestamp used to expire stale sessions.
    """

    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    session_id = Column(String, unique=True, index=True, nullable=False)
    topic = Column(String, nullable=True)
    last_question = Column(Text, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<UserSession(user_id={self.user_id}, "
            f"session_id={self.session_id}, topic={self.topic})>"
        )
