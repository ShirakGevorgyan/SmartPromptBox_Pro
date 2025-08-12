"""Aiogram middleware: inject a short correlation/request id per update.

Adds `data["req_id"]` (8-hex string) so logs across middlewares/handlers
can be tied together when troubleshooting.
"""

import uuid
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class RequestId(BaseMiddleware):
    """Middleware that sets `req_id` in the per-update `data` dict."""

    async def __call__(self, handler, event: TelegramObject, data: dict):
        """Generate and attach a short request id, then call downstream.

        Args:
            handler: Next callable in the pipeline.
            event: Incoming update object.
            data: Mutable context dict for this update.

        Returns:
            The downstream handler result.
        """
        data["req_id"] = uuid.uuid4().hex[:8]
        return await handler(event, data)
