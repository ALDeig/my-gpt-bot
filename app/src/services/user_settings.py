from app.src.services.db.dao.holder import HolderDao
from app.src.services.db.models import Settings


async def get_open_ai_settings(dao: HolderDao, user_id: int) -> Settings:
    return await dao.settings.find_one(id=user_id)


async def answer_update_setting(
    dao: HolderDao, user_id: int, setting_type: str, value: str
) -> Settings:
    await dao.settings.update({setting_type: value}, user_id=user_id)
    return await get_open_ai_settings(dao, user_id)
