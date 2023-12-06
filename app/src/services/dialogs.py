from aiogram import html
from aiogram.types import BufferedInputFile, InputFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db import db_requests
from app.src.services.db.models import TTSVoice
from app.src.services.openai import (
    get_image_from_gpt,
    get_response_from_gpt,
    text_to_speech,
)


async def get_messages_to_request(
    session: AsyncSession, user_id: int, text: str
) -> list[dict[str, str]]:
    """Получение сообщений для в openai из базы и соединение их с текущим запросом"""
    dialogs = await db_requests.get_dialogs(session, user_id)
    messages = []
    for dialog in dialogs:
        messages.append({"role": dialog.role, "content": dialog.content})
    messages.append({"role": "user", "content": text})
    await db_requests.add_dialog(session, user_id, "user", text)
    return messages


async def add_role_for_dialog(session: AsyncSession, user_id: int, text: str):
    """Довабление роли для диалога в базу данных"""
    await db_requests.add_dialog(session, user_id, "system", text)


async def response_from_gpt(session: AsyncSession, user_id: int, message: str) -> str:
    """Получение ответа от openai, сохранение его в БД"""
    messages_to_request = await get_messages_to_request(session, user_id, message)
    response = await get_response_from_gpt(messages_to_request)
    if response is None:
        return "Не удалось получить ответ"
    response = html.quote(response)
    await db_requests.add_dialog(session, user_id, "assistant", response)
    return response


async def response_audio(
    session: AsyncSession, user_id: int, text: str
) -> InputFile | None:
    """Получает аудио данные от openai и подготовливает
    их для отправки пользователя через ТГ"""
    settings = await db_requests.get_settings(session, user_id)
    if settings.tts_voice == TTSVoice.NOT_SELECT:
        return
    response = await text_to_speech(text, settings.tts_voice.value)
    return BufferedInputFile(response, "audio")


async def generate_image(session: AsyncSession, user_id: int, text: str) -> str | None:
    settings = await db_requests.get_settings(session, user_id)
    image_url = await get_image_from_gpt(
        text, settings.image_format.value, settings.image_style.value
    )
    return image_url


async def clear_dialog_context(session: AsyncSession, user_id: int):
    """Очистка истории диалога и роли"""
    await db_requests.remove_dialogs_by_user_id(session, user_id)


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
