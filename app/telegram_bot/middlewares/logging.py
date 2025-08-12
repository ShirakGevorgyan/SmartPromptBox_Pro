import logging
import time
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

log = logging.getLogger(__name__)


class LogUpdate(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
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
