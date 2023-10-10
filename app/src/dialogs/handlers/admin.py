from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.dialogs import (
    clear_dialog_context,
    get_messages_to_request,
    response_from_gpt,
)
from app.src.services.user import save_user


router = Router()


@router.message(Command(commands="start"), flags={"db": True})
async def cmd_start(msg: Message, db: AsyncSession, state: FSMContext):
    if msg.from_user is None:
        return
    await state.clear()
    await save_user(db, msg.chat.id, msg.from_user.full_name, msg.from_user.username)
    await msg.answer("Пришли свой запрос...")


@router.message(Command(commands="clear"), flags={"db": True})
async def cmd_clear_dialog(msg: Message, db: AsyncSession):
    await clear_dialog_context(db, msg.chat.id)
    await msg.answer("Контекст очищен")


@router.message(flags={"db": True})
async def get_request(msg: Message, db: AsyncSession):
    if msg.text is None:
        return
    messages_to_request = await get_messages_to_request(db, msg.chat.id, msg.text)
    response = await response_from_gpt(db, msg.chat.id, messages_to_request)
    await msg.answer(response)
