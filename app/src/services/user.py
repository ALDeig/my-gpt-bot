

from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db import db_requests


async def save_user(session: AsyncSession, user_id: int):
    await db_requests.add_user(session, user_id)
