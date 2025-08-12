import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

log = logging.getLogger(__name__)


class CatchAllErrors(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            log.exception("handler_error: %r", e)
            if isinstance(event, Message):
                try:
                    await event.answer(
                        "Ուֆ, մի բան սխալվեց 🤔 Փորձիր նորից մի քիչ հետո։"
                    )
                except Exception as exc:
                    # չլռենք՝ բայց չխափանենք հոսքը
                    log.debug("Failed to send error message to user: %s", exc)
            return None
