from app.src.services.db.dao.holder import HolderDao
from app.src.services.db.models import Settings


async def get_open_ai_settings(dao: HolderDao, user_id: int) -> Settings:
    settings = await dao.settings.find_one_or_none(id=user_id)
    if settings is None:
        settings = await dao.settings.add(Settings(id=user_id))
    return settings


async def answer_update_setting(
    dao: HolderDao, user_id: int, setting_type: str, value: str
) -> Settings:
    await dao.settings.update({setting_type: value}, id=user_id)
    return await get_open_ai_settings(dao, user_id)
