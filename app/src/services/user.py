from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db import db_requests


async def save_user(
    session: AsyncSession, user_id: int, name: str, username: str | None
):
    """Сохранение пользователя в базу данных. Функция вызывается при вводе команды
    start"""
    await db_requests.add_user(session, user_id, name, username)
