from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db.tables import Dialog, User


async def add_user(
    session: AsyncSession, user_id: int, name: str, username: str | None
):
    """Добавление пользователя в БД"""
    stmt = (
        insert(User)
        .values(id=user_id, name=name, username=username)
        .on_conflict_do_nothing(index_elements=[User.id])
    )
    await session.execute(stmt)
    await session.commit()


async def get_dialogs(session: AsyncSession, user_id: int) -> Sequence[Dialog]:
    """Получение истории диалога из БД. Несколько сохраненных записей в базе,
    упорядоченных по ID"""
    stmt = sa.select(Dialog).where(Dialog.user_id == user_id).order_by(Dialog.id)
    dialogs = await session.scalars(stmt)
    return dialogs.all()


async def add_dialog(session: AsyncSession, user_id: int, role: str, content: str):
    """Сохранение сообщения или роли в БД"""
    session.add(Dialog(user_id=user_id, role=role, content=content))
    await session.commit()


async def remove_dialogs_by_user_id(session: AsyncSession, user_id: int):
    """Очистка истории диалога и роли"""
    await session.execute(sa.delete(Dialog).where(Dialog.user_id == user_id))
    await session.commit()
