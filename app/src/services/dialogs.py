from aiogram import html
from aiogram.types import BufferedInputFile, InputFile

from app.src.services.db.dao.holder import HolderDao
from app.src.services.db.models import Dialog, TTSVoice
from app.src.services.markdown import escape_special_characters_in_place_text
from app.src.services.openai import (
    get_image_from_gpt,
    get_response_from_gpt,
    text_to_speech,
)


async def _get_messages_to_request(
    dao: HolderDao, user_id: int, text: str
) -> list[dict[str, str]]:
    """Получение сообщений для в openai из базы и соединение их с текущим запросом."""
    dialogs = await dao.dialog.find_all(user_id=user_id)
    messages = [{"role": dialog.role, "content": dialog.content} for dialog in dialogs]
    messages.append({"role": "user", "content": text})
    await dao.dialog.add(Dialog(user_id=user_id, role="user", content=text))
    return messages


async def add_role_for_dialog(dao: HolderDao, user_id: int, text: str):
    """Довабление роли для диалога в базу данных."""
    await dao.dialog.add(Dialog(user_id=user_id, role="system", content=text))


async def response_from_gpt(dao: HolderDao, user_id: int, message: str) -> str:
    """Получение ответа от openai, сохранение его в БД."""
    messages_to_request = await _get_messages_to_request(dao, user_id, message)
    response = await get_response_from_gpt(messages_to_request)
    if response is None:
        return "Не удалось получить ответ"
    await dao.dialog.add(
        Dialog(user_id=user_id, role="assistant", content=html.quote(response))
    )
    return escape_special_characters_in_place_text(response)


async def response_audio(
    dao: HolderDao, user_id: int, text: str
) -> InputFile | None:
    """Получает аудио данные от openai и подготовливает
    их для отправки пользователя через ТГ.
    """
    settings = await dao.settings.find_one(id=user_id)
    if settings.tts_voice == TTSVoice.NOT_SELECT:
        return
    response = await text_to_speech(text, settings.tts_voice.value)
    return BufferedInputFile(response, "audio")


async def generate_image(dao: HolderDao, user_id: int, text: str) -> str | None:
    settings = await dao.settings.find_one(id=user_id)
    return await get_image_from_gpt(
        text, settings.image_format.value, settings.image_style.value
    )


async def clear_dialog_context(dao: HolderDao, user_id: int):
    """Очистка истории диалога и роли."""
    await dao.dialog.delete(user_id=user_id)


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
