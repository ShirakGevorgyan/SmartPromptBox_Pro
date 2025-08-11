import uuid
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class RequestId(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        data["req_id"] = uuid.uuid4().hex[:8]
        return await handler(event, data)
