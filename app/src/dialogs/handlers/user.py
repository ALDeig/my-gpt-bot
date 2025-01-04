from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.settings import settings
from app.src.dialogs.keyboards.user import web_app_keyboard
from app.src.services.db.dao.holder import HolderDao
from app.src.services.user import save_user

router = Router()


@router.message(Command(commands="start"), flags={"dao": True})
async def cmd_start(msg: Message, dao: HolderDao, state: FSMContext):
    await state.clear()
    await save_user(dao, msg.chat.id, msg.chat.full_name, msg.chat.username)
    if msg.chat.id in settings.ADMINS:
        await msg.answer("Добро пожаловать в MyGPT!", reply_markup=web_app_keyboard())
