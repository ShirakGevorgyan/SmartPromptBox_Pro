"""SQLAlchemy Declarative Base.

This module exposes a single `Base` that all ORM models should inherit from.
Keeping it in one place avoids circular imports and ensures metadata is shared.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
