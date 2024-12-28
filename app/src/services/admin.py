from collections.abc import Sequence

from app.src.services.db.dao.holder import HolderDao
from app.src.services.db.models import AIModel
from app.src.services.openai.enums import ModelSource


def get_model_sources() -> list[str]:
    return list(ModelSource)


async def add_model(dao: HolderDao, source: str, model: str, description: str) -> None:
    await dao.ai_model.add(
        AIModel(source=ModelSource(source), model=model, description=description)
    )


async def get_models(dao: HolderDao) -> Sequence[AIModel]:
    return await dao.ai_model.find_all()


async def delete_model(dao: HolderDao, model_id: int) -> None:
    await dao.ai_model.delete(id=model_id)
