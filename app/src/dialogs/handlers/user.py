from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.user import save_user

router = Router()


@router.message(Command(commands="start"), flags={"db": True})
async def cmd_start(msg: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    await save_user(db, msg.chat.id, msg.chat.full_name, msg.chat.username)
    # await msg.answer(f"Hello {html.quote(msg.from_user.full_name)}!")
