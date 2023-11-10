from aiogram import html
from aiogram.types import BufferedInputFile, InputFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db import db_requests
from app.src.services.openai import get_response_from_gpt, text_to_speech


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


async def response_from_gpt(
    session: AsyncSession, user_id: int, messages: list[dict[str, str]]
) -> str:
    """Получение ответа от openai, сохранение его в БД"""
    response = await get_response_from_gpt(messages)
    if response is None:
        return "Не удалось получить ответ"
    response = html.quote(response)
    await db_requests.add_dialog(session, user_id, "assistant", response)
    return response


async def response_audio(text: str) -> InputFile:
    response = await text_to_speech(text)
    return BufferedInputFile(response, "audio")


async def clear_dialog_context(session: AsyncSession, user_id: int):
    """Очистка истории диалога и роли"""
    await db_requests.remove_dialogs_by_user_id(session, user_id)
