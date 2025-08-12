"""Minimal logging configuration helper.

Respects LOG_LEVEL from the environment (default: INFO) and sets a concise
timestamped format suitable for local runs and CI logs.
"""

import logging
import os

LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logging() -> None:
    """Initialize the root logger with level and simple formatter."""
    logging.basicConfig(
        level=LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
