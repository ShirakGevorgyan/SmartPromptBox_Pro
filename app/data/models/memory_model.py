"""SQLAlchemy model for per-message conversation memory.

Each row stores an individual message (role + content) and a few optional
metadata fields to help with personalization and later summarization.
"""

from sqlalchemy import Column, Integer, String, Text

from app.data.models.base import Base


class UserMemory(Base):
    """Conversation memory row.

    Attributes:
        user_id: Telegram user identifier.
        role: 'user' | 'assistant' | 'system'.
        content: Raw message content (may be summarized later).
        user_name: Optional display name.
        bot_name: Optional bot display name (at the time of message).
        last_mood: Optional last detected mood tag.
        history: Optional serialized thread context (JSON or text).
    """

    __tablename__ = "user_memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)

    role = Column(String)
    content = Column(Text)

    user_name = Column(String, nullable=True)
    bot_name = Column(String, nullable=True)
    last_mood = Column(String, nullable=True)
    history = Column(Text, nullable=True)
