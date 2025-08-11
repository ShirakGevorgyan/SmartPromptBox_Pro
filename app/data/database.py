# app/data/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models.base import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db/memory.db")

# SQLite-ի դեպքում check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
