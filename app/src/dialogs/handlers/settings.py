from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


router = Router()


@router.message(Command("settings"))
async def cmd_settings(msg: Message, state: FSMContext):
    kb = kb_choice_setting()
    await msg.answer("Ваши настройки: ... Что изменить?")
