import logging
import os

LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def setup_logging() -> None:
    logging.basicConfig(
        level=LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
