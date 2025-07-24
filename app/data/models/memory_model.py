
from app.data.models.base import Base
from sqlalchemy import Column, Integer, String, Text

class UserMemory(Base):
    __tablename__ = "user_memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)

    role = Column(String)  # 'user' կամ 'assistant'
    content = Column(Text)

    # ✅ Ավելացված դաշտեր
    user_name = Column(String, nullable=True)
    bot_name = Column(String, nullable=True)
    last_mood = Column(String, nullable=True)
    history = Column(Text, nullable=True)
