"""Aiogram middleware: structured request logging with latency.

Captures:
- `req_id` from `data` (if present; see RequestId middleware),
- event type (Message/CallbackQuery),
- chat_id, user_id,
- a short preview of text/data (max 80 chars, ellipsis appended),
- handler latency in milliseconds.

Logs a single line on completion at INFO level.
"""

import logging
import time
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

log = logging.getLogger(__name__)


class LogUpdate(BaseMiddleware):
    """Middleware that logs a compact line for every handled update."""

    async def __call__(self, handler, event: TelegramObject, data: dict):
        """Measure duration, collect context, call handler, then log.

        The preview is:
            - message text (truncated to 80 chars) for `Message`,
            - callback data (truncated to 80 chars) for `CallbackQuery`,
            - otherwise `None`.

        Args:
            handler: Next callable in the chain.
            event: Incoming update (message/callback/etc).
            data: Mutable per-update context dict (may contain `req_id`).

        Returns:
            Whatever the downstream handler returns.
        """
        t0 = time.perf_counter()
        req_id = data.get("req_id")

        chat_id = None
        user_id = None
        preview = None

        if isinstance(event, Message):
            chat_id = getattr(getattr(event, "chat", None), "id", None)
            user_id = getattr(getattr(event, "from_user", None), "id", None)
            if event.text:
                preview = (
                    (event.text[:80] + "…")
                    if len(event.text or "") > 80
                    else event.text
                )
        elif isinstance(event, CallbackQuery):
            chat_id = (
                getattr(getattr(event.message, "chat", None), "id", None)
                if event.message
                else None
            )
            user_id = getattr(getattr(event, "from_user", None), "id", None)
            preview = (
                (event.data[:80] + "…")
                if event.data and len(event.data) > 80
                else event.data
            )

        try:
            return await handler(event, data)
        finally:
            dt_ms = (time.perf_counter() - t0) * 1000
            log.info(
                "req_id=%s handled=%s chat_id=%s user_id=%s dt_ms=%.1f preview=%r",
                req_id,
                type(event).__name__,
                chat_id,
                user_id,
                dt_ms,
                preview,
            )
