from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.data.models.session_model import UserSession

SESSION_TIMEOUT = 60 * 30


def get_or_create_user_session(db: Session, user_id: str) -> str:
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
    try:
        session = db.query(UserSession).filter_by(user_id=user_id).first()
        if session:
            return session.topic, session.last_question
        return None, None
    except Exception as e:
        print(f"❌ Error in get_session_info: {e}")
        return None, None
