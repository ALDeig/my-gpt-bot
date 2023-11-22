import sqlalchemy as sa

from app.settings import settings
from app.src.services.db.db_connect import create_session_factory
from app.src.services.db.db_requests import BaseDAO
from app.src.services.db.tables import Settings


session_factory = create_session_factory(str(settings.sqlite_dsn))


class SettingsDAO(BaseDAO):
    @classmethod
    async def get_settings(cls, user_id: int) -> Settings:
        response = await cls.find_one_or_none(Settings, user_id=user_id)
        if response is None:
            response = await cls.add(Settings, user_id=user_id)
            return response
        return response

    @classmethod
    async def update_settings(cls, user_id: int, update_fields: dict):
        async with session_factory() as session:
            query = (
                sa.update(Settings)
                .where(Settings.user_id == user_id)
                .values(**update_fields)
            )
            await session.execute(query)
            await session.commit()
