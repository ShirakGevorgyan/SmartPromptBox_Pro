"""Minimal conversation memory service.

Stores and retrieves per-user message history in the `UserMemory` table.
The in/out format mirrors OpenAI chat messages:
`[{ "role": "...", "content": "..." }, ...]`.
"""

from typing import List, Dict
from sqlalchemy.orm import Session
from app.data.models.memory_model import UserMemory


def load_history(session: Session, user_id: str) -> List[Dict[str, str]]:
    """Load full history for a user as a list of role/content dicts.

    Args:
        session: Open SQLAlchemy session.
        user_id: Telegram user identifier as string.

    Returns:
        List of dicts shaped like: `[{ "role": str, "content": str }, ...]`,
        ordered by insertion (ascending id).
    """
    messages = (
        session.query(UserMemory)
        .filter_by(user_id=user_id)
        .order_by(UserMemory.id.asc())
        .all()
    )
    return [{"role": msg.role, "content": msg.content} for msg in messages]


def save_history(session: Session, user_id: str, history: List[Dict[str, str]]):
    """Replace the user's history with the provided messages.

    Workflow:
        1) Delete existing rows for the given `user_id`.
        2) Insert rows based on the provided `history` list.
        3) Commit.

    Args:
        session: Open SQLAlchemy session.
        user_id: Telegram user identifier as string.
        history: List of dicts: `{"role": str, "content": str}`.
    """
    session.query(UserMemory).filter_by(user_id=user_id).delete()
    session.commit()

    for item in history:
        msg = UserMemory(user_id=user_id, role=item["role"], content=item["content"])
        session.add(msg)
    session.commit()
