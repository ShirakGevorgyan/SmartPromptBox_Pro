"""Aiogram middleware: catch all unhandled exceptions.

This middleware:
- Logs the exception with stacktrace.
- If the update is a `Message`, attempts to inform the user in Armenian with a
friendly error text (best-effort; failures are swallowed and debug-logged).
- Prevents the exception from bubbling up and breaking the update pipeline.
"""

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

log = logging.getLogger(__name__)


class CatchAllErrors(BaseMiddleware):
    """Middleware that wraps the next handler in a try/except guard."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """Execute downstream handler and intercept failures.

        On exception:
            - Log with `log.exception`.
            - If `event` is a `Message`, try to send a short user-facing notice.
            - Return `None` to indicate the failure was handled.

        Args:
            handler: The next callable in the middleware chain.
            event: The current update (message/callback/etc).
            data: Per-update context dict.

        Returns:
            The downstream handler result, or `None` on error.
        """
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
                    log.debug("Failed to send error message to user: %s", exc)
            return None
