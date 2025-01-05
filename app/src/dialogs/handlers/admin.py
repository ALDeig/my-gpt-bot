from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.src.dialogs.keyboards.user import web_app_keyboard
from app.src.services.db.dao.holder import HolderDao
from app.src.services.user import save_user

router = Router()


@router.message(Command(commands="start"), flags={"dao": True})
async def cmd_start(msg: Message, dao: HolderDao, state: FSMContext):
    """Хендлер на команду /start. Очищает состояние, сохраняет пользователя в БД."""
    if msg.from_user is None:
        return
    await state.clear()
    await save_user(dao, msg.chat.id, msg.from_user.full_name, msg.from_user.username)
    await msg.answer(
        "Пришли свой запрос...", reply_markup=web_app_keyboard(msg.chat.id)
    )
