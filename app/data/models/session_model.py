from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.data.models.base import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    session_id = Column(String, unique=True, index=True, nullable=False)
    topic = Column(String, nullable=True)
    last_question = Column(Text, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<UserSession(user_id={self.user_id}, session_id={self.session_id}, topic={self.topic})>"
