from typing import Literal

from aiogram.types import BufferedInputFile, InputFile

from app.src.services.db.dao.holder import HolderDao
from app.src.services.db.models import AIChatMessage, Chat
from app.src.services.exceptions import ChatIsExistError, ModelNotSelectedError
from app.src.services.markdown import escape_special_characters_in_place_text
from app.src.services.openai.openai import (
    get_image_from_gpt,
    get_response_from_gpt,
    text_to_speech,
)
from app.src.services.user_settings import get_open_ai_settings


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


async def add_role_for_dialog(dao: HolderDao, user_id: int, text: str):
    """Довабление роли для диалога в базу данных."""
    chat = await dao.chat.find_one_or_none(user_id=user_id, type="bot")
    if chat:
        raise ChatIsExistError
    chat = await create_chat(dao, user_id, "bot")
    await dao.ai_chat_message.add(
        AIChatMessage(chat_id=chat.id, role="developer", content=text)
    )


async def create_chat(dao: HolderDao, user_id: int, chat_type: Literal["bot", "app"]):
    settings = await get_open_ai_settings(dao, user_id)
    if not settings.gpt_model_id:
        raise ModelNotSelectedError
    return await dao.chat.add(
        Chat(user_id=user_id, model_id=settings.gpt_model_id, type=chat_type)
    )


async def response_from_gpt(dao: HolderDao, user_id: int, message: str) -> str:
    """Получение ответа от openai, сохранение его в БД."""
    chat = await dao.chat.find_one_or_none(user_id=user_id, type="bot")
    if not chat:
        chat = await create_chat(dao, user_id, "bot")
        await chat.awaitable_attrs.messages
    messages = await _get_messages_to_request(dao, chat, message)
    ai_model = await dao.ai_model.find_one_or_none(id=chat.model_id)
    if not ai_model:
        raise ModelNotSelectedError
    response = await get_response_from_gpt(messages, ai_model.model)
    if response is None:
        return "Не удалось получить ответ"
    await dao.ai_chat_message.add(
        AIChatMessage(chat_id=chat.id, role="assistant", content=response)
    )
    return escape_special_characters_in_place_text(response)


async def response_audio(dao: HolderDao, user_id: int, text: str) -> InputFile | None:
    """Получает аудио данные от openai и подготовливает
    их для отправки пользователя через ТГ.
    """
    settings = await get_open_ai_settings(dao, user_id)
    if settings.tts_voice is None:
        return
    response = await text_to_speech(text, settings.tts_voice)
    return BufferedInputFile(response, "audio")


async def generate_image(dao: HolderDao, user_id: int, text: str) -> str | None:
    settings = await get_open_ai_settings(dao, user_id)
    if settings.dalle_model is None:
        raise ModelNotSelectedError
    return await get_image_from_gpt(
        text, settings.image_format, settings.image_style, settings.dalle_model.model
    )


async def clear_dialog_context(dao: HolderDao, user_id: int):
    """Очистка истории диалога и роли."""
    chat = await dao.chat.find_one_or_none(user_id=user_id, type="bot")
    if chat:
        await dao.ai_chat_message.delete(chat_id=chat.id)
        await dao.chat.delete(id=chat.id)


# async def show_generation_status(wait_message: Message):
#     """Создает динамичное сообщение со сменающимися статусами обработки запроса"""
#     animation_frames = [
#         "⠀\n⏳ Запрос принят в обработку...\n⠀",
#         "⠀\n❇️ Готовится ответ...\n⠀",
#         # "⠀\n🗣 Синтезируется голос...\n⠀",
#     ]
#     frame_index = 0
#     while True:
#         await asyncio.sleep(1)
#         try:
#             await wait_message.edit_text(animation_frames[frame_index])
#             frame_index = (frame_index + 1) % len(animation_frames)
#         except TelegramRetryAfter:
#             await asyncio.sleep(1)
#         except TelegramBadRequest:
#             frame_index = (frame_index + 1) % len(animation_frames)
#             await wait_message.answer(animation_frames[frame_index])
