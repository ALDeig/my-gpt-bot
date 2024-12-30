from collections.abc import Sequence

import sqlalchemy as sa

from app.src.services.db.dao.base_dao import BaseDao
from app.src.services.db.models import AIChatMessage, AIModel, Chat, Settings, User


class AiChatMessageDao(BaseDao[AIChatMessage]):
    """DAO для работы с сообщениями c ИИ."""

    model = AIChatMessage


class UserDao(BaseDao[User]):
    """DAO для работы с пользователями."""

    model = User


class ChatDao(BaseDao[Chat]):
    """DAO для работы с чатами."""

    model = Chat


class SettingDao(BaseDao[Settings]):
    """DAO для работы с настройками."""

    model = Settings


class AIModelDao(BaseDao):
    """DAO для работы с моделями."""

    model = AIModel

    async def unique_sources(self) -> Sequence[str]:
        query = sa.select(AIModel.source)
        response = await self._session.scalars(query)
        return response.unique().all()
