import logging
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db.dao.base_dao import BaseDao
from app.src.services.db.dao.dao import (
    AiChatMessageDao,
    AIModelDao,
    ChatDao,
    SettingDao,
    UserDao,
)
from app.src.services.db.dao.exceptions import DaoNotFoundError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseDao)


class HolderDao:
    """Содержит или инициализирует все экземпляры DAO."""

    __slots__ = (
        "_ai_chat_message",
        "_ai_model",
        "_chat",
        "_session",
        "_settings",
        "_user",
    )

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._ai_chat_message: AiChatMessageDao | None = None
        self._ai_model: AIModelDao | None = None
        self._chat: ChatDao | None = None
        self._settings: SettingDao | None = None
        self._user: UserDao | None = None

    @property
    def ai_model(self) -> AIModelDao:
        return self._get_dao("ai_model", AIModelDao)

    @property
    def chat(self) -> ChatDao:
        return self._get_dao("chat", ChatDao)

    @property
    def ai_chat_message(self) -> AiChatMessageDao:
        return self._get_dao("ai_chat_message", AiChatMessageDao)

    @property
    def settings(self) -> SettingDao:
        return self._get_dao("settings", SettingDao)

    @property
    def user(self) -> UserDao:
        return self._get_dao("user", UserDao)

    def _get_dao(self, dao_name: str, dao: type[T]) -> T:
        try:
            val = getattr(self, f"_{dao_name}")
        except AttributeError as er:
            logger.exception("Not field %s for DAO object", dao_name)
            raise DaoNotFoundError from er
        if not val:
            val = dao(self._session)
            setattr(self, f"_{dao_name}", val)
        return val
