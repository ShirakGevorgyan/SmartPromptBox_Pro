from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models.base import Base  # Միակ ընդհանուր Base-ը
from app.data.models.memory_model import UserMemory
from app.data.models.session_model import UserSession

DATABASE_URL = "sqlite:///db/memory.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db():
    Base.metadata.create_all(bind=engine)
