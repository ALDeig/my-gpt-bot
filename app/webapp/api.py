from pydantic import BaseModel, Field, field_validator

from app.src.services.db.base import session_factory
from app.src.services.db.dao.holder import HolderDao
from app.src.services.db.models import AIChatMessage, AIModel, Chat
from app.src.services.openai.openai import get_response_from_gpt


class SNewChat(BaseModel):
    """Модель нового чата."""

    model_config = {"protected_namespaces": ()}

    model_id: int = Field(alias="modelId")
    user_id: int = Field(alias="userId")


class SMessage(BaseModel):
    """Модель сообщения."""

    id: int
    role: str
    content: str


class SChat(BaseModel):
    """Модель чата."""

    model_config = {"protected_namespaces": ()}

    id: int
    user_id: int = Field(serialization_alias="userId")
    model_id: int = Field(serialization_alias="modelId")
    model: str
    messages: list[SMessage]

    @field_validator("model", mode="before")
    @classmethod
    def model_validator(cls, model: AIModel) -> str:
        return model.model


class SAIModel(BaseModel):
    """Модель модели."""

    id: int
    source: str
    model: str
    description: str


async def get_app_chats(user_id: int) -> list[SChat]:
    async with session_factory() as session:
        chats = await HolderDao(session).chat.find_all(user_id=user_id, type="app")
    return [SChat.model_validate(chat, from_attributes=True) for chat in chats]


async def get_ai_models() -> list[SAIModel]:
    async with session_factory() as session:
        models = await HolderDao(session).ai_model.find_all()
    return [SAIModel.model_validate(model, from_attributes=True) for model in models]


async def create_new_chat(new_chat: SNewChat) -> SChat:
    async with session_factory() as session:
        dao = HolderDao(session)
        chat = await dao.chat.add(
            Chat(user_id=new_chat.user_id, model_id=new_chat.model_id, type="app")
        )
        await chat.awaitable_attrs.model
        await chat.awaitable_attrs.messages
        return SChat.model_validate(chat, from_attributes=True)


async def get_chat(chat_id: int) -> SChat:
    async with session_factory() as session:
        dao = HolderDao(session)
        chat = await dao.chat.find_one_or_none(id=chat_id)
    return SChat.model_validate(chat, from_attributes=True)


async def remove_chat(chat_id: int) -> None:
    async with session_factory() as session:
        dao = HolderDao(session)
        await dao.ai_chat_message.delete(chat_id=chat_id)
        await dao.chat.delete(id=chat_id)


async def gpt_request(chat_id: int, text: str) -> str:
    async with session_factory() as session:
        dao = HolderDao(session)
        chat = await dao.chat.find_one_or_none(id=chat_id)
        if not chat:
            return ""
        messages = await _get_messages_to_request(dao, chat, text)
        resp = await get_response_from_gpt(messages, chat.model.model)
        if not resp:
            return ""
        await dao.ai_chat_message.add(
            AIChatMessage(chat_id=chat.id, role="assistant", content=resp)
        )
        return resp


async def _get_messages_to_request(
    dao: HolderDao, chat: Chat, text: str
) -> list[dict[str, str]]:
    """Получение сообщений для в openai из базы и соединение их с текущим запросом."""
    request_format_messages = [
        {"role": message.role, "content": message.content} for message in chat.messages
    ]
    request_format_messages.append({"role": "user", "content": text})
    await dao.ai_chat_message.add(
        AIChatMessage(chat_id=chat.id, role="user", content=text)
    )
    return request_format_messages
