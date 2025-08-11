import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models.base import Base

# .env-ում կարող ես թողնել DATABASE_URL, հակառակ դեպքում կօգտագործվի sqlite տեղում
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db/memory.db")

IS_SQLITE = DATABASE_URL.startswith("sqlite")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if IS_SQLITE else {},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

def init_db() -> None:
    """Ստեղծում է db/ պանակը և աղյուսակները, եթե չկան."""
    if IS_SQLITE:
        Path("db").mkdir(parents=True, exist_ok=True)

    # ՄՈԴԵԼՆԵՐԻ ԻՄՊՈՐՏ — կարևորը, որ աղյուսակները գրանցվեն Base.metadata-ում
    from app.data.models import session_model  # noqa: F401
    # եթե ունես այլ մոդելներ, այստեղ էլ імпорт արա (քոմենթը պահիր)

    Base.metadata.create_all(bind=engine)

# օգտակար՝ եթե երբևէ պետք լինի scoped session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
