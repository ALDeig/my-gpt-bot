from collections.abc import Callable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject

from app.src.services.db.base import session_factory
from app.src.services.db.dao.holder import HolderDao


class DbSessionMiddleware(BaseMiddleware):
    """Middleware для работы с базой данных."""

    def __init__(self) -> None:
        super().__init__()

    async def __call__(
        self, handler: Callable, event: TelegramObject, data: dict
    ) -> None:
        if not get_flag(data, "dao"):
            return await handler(event, data)
        async with session_factory() as session:
            data["dao"] = HolderDao(session)
            return await handler(event, data)
