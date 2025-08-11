import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

log = logging.getLogger(__name__)

class CatchAllErrors(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        try:
            return await handler(event, data)
        except Exception as e:
            log.exception("handler_error: %r", e)
            if isinstance(event, Message):
                try:
                    await event.answer("Ուֆ, մի բան սխալվեց 🤔 Փորձիր նորից մի քիչ հետո։")
                except Exception:
                    pass
            return None
