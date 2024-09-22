import logging
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db.dao.base_dao import BaseDao
from app.src.services.db.dao.dao import DialogDao, SettingDao, UserDao
from app.src.services.db.dao.exceptions import DaoNotFoundError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseDao)


class HolderDao:
    """Содержит или инициализирует все экземпляры DAO."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._dialog: DialogDao | None = None
        self._settings: SettingDao | None = None
        self._user: UserDao | None = None

    @property
    def dialog(self) -> DialogDao:
        return self._get_dao("dialog", DialogDao)

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
