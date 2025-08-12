"""Lightweight per-user session tracking helpers.

Functions:
    - get_or_create_user_session: return an active `session_id` or create a new one.
    - update_session_info: upsert `topic` and `last_question` for the user session.
    - get_session_info: fetch `(topic, last_question)` tuple for the user.
"""

from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.data.models.session_model import UserSession

SESSION_TIMEOUT = 60 * 30


def get_or_create_user_session(db: Session, user_id: str) -> str:
    """Return an active session_id for the given user, creating a new one if needed.

    Logic:
        - If a session exists and is still fresh (last_seen within SESSION_TIMEOUT),
        refresh `last_seen` and reuse its `session_id`.
        - Otherwise, delete the stale session (if any) and create a new one.

    Args:
        db: Open SQLAlchemy session.
        user_id: Telegram user identifier as string.

    Returns:
        The active `session_id` for this user.

    Raises:
        Exception: Re-raises any DB error after rollback.
    """
    now = datetime.utcnow()
    session = db.query(UserSession).filter_by(user_id=user_id).first()

    try:
        if session:
            delta = (now - session.last_seen).total_seconds()
            if delta < SESSION_TIMEOUT:
                session.last_seen = now
                db.commit()
                return session.session_id
            else:
                db.delete(session)
                db.commit()

        new_session_id = str(uuid.uuid4())
        new_session = UserSession(
            user_id=user_id, session_id=new_session_id, last_seen=now
        )
        db.add(new_session)
        db.commit()
        return new_session_id

    except Exception as e:
        db.rollback()
        print(f"❌ Error in get_or_create_user_session: {e}")
        raise


def update_session_info(
    db: Session, user_id: str, topic: str = None, last_question: str = None
):
    """Update or create a user session with auxiliary fields.

    If a row exists:
        - Update `last_seen`.
        - Optionally update `topic` and/or `last_question`.

    If a row does not exist:
        - Create a new session initialized with provided values.

    Args:
        db: Open SQLAlchemy session.
        user_id: Telegram user identifier as string.
        topic: Optional topical label/category.
        last_question: Optional text of the user's most recent question.

    Raises:
        Exception: Re-raises any DB error after rollback.
    """
    try:
        session = db.query(UserSession).filter_by(user_id=user_id).first()
        if session:
            session.last_seen = datetime.utcnow()
            if topic:
                session.topic = topic
            if last_question:
                session.last_question = last_question
        else:
            # fallback
            session = UserSession(
                user_id=user_id,
                session_id=str(uuid.uuid4()),
                last_seen=datetime.utcnow(),
                topic=topic,
                last_question=last_question,
            )
            db.add(session)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"❌ Error in update_session_info: {e}")
        raise


def get_session_info(db: Session, user_id: str):
    """Return `(topic, last_question)` for the current user session.

    If no session exists, returns `(None, None)`.

    Args:
        db: Open SQLAlchemy session.
        user_id: Telegram user identifier as string.

    Returns:
        Tuple[str|None, str|None]: `(topic, last_question)` or `(None, None)`.
    """
    try:
        session = db.query(UserSession).filter_by(user_id=user_id).first()
        if session:
            return session.topic, session.last_question
        return None, None
    except Exception as e:
        print(f"❌ Error in get_session_info: {e}")
        return None, None
