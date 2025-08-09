from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models.base import Base

DATABASE_URL = "sqlite:///db/memory.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
