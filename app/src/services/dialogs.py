from aiogram import html
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db import db_requests
from app.src.services.openai import get_response_from_gpt


async def get_messages_to_request(
    session: AsyncSession, user_id: int, text: str
) -> list[dict[str, str]]:
    dialogs = await db_requests.get_dialogs(session, user_id)
    messages = []
    for dialog in dialogs:
        messages.append({"role": dialog.role, "content": dialog.content})
    messages.append({"role": "user", "content": text})
    await db_requests.add_dialog(session, user_id, "user", text)
    return messages


async def response_from_gpt(
    session: AsyncSession, user_id: int, messages: list[dict[str, str]]
) -> str:
    response = html.quote(await get_response_from_gpt(messages))
    await db_requests.add_dialog(session, user_id, "assistant", response)
    return response


async def clear_dialog_context(session: AsyncSession, user_id: int):
    await db_requests.remove_dialogs_by_user_id(session, user_id)
