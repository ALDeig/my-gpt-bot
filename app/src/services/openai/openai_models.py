from collections.abc import Sequence

from app.src.services.db.dao.holder import HolderDao
from app.src.services.db.models import AIModel
from app.src.services.openai.enums import ModelSource


async def get_models(dao: HolderDao) -> Sequence[AIModel]:
    """Получение списка доступных моделей."""
    return await dao.ai_model.find_all()


async def get_models_by_source(
    dao: HolderDao, source: ModelSource
) -> Sequence[AIModel]:
    """Получение списка доступных моделей."""
    return await dao.ai_model.find_all(source=source)
