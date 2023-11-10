from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.dialogs import (
    add_role_for_dialog,
    clear_dialog_context,
    get_messages_to_request,
    response_audio,
    response_from_gpt,
)
from app.src.services.openai import text_to_speech
from app.src.services.user import save_user


router = Router()


@router.message(Command(commands="start"), flags={"db": True})
async def cmd_start(msg: Message, db: AsyncSession, state: FSMContext):
    """Хендлер на команду /start. Очищает состояние, сохраняет пользователя в БД"""
    if msg.from_user is None:
        return
    await state.clear()
    await save_user(db, msg.chat.id, msg.from_user.full_name, msg.from_user.username)
    await msg.answer("Пришли свой запрос...")


@router.message(Command(commands="add_role"))
async def cmd_add_role(msg: Message, state: FSMContext):
    """Хендлер на команду /add_role (добавить роль). Устанавливает состояние для 
    добавления роли"""
    await msg.answer("Напишите роль в которой должен общаться ChatGPT")
    await state.set_state("get_role")


@router.message(StateFilter("get_role"), flags={"db": True})
async def get_role(msg: Message, db: AsyncSession, state: FSMContext):
    """Сообщение с ролью. Сохраняет роль"""
    if msg.text is None:
        return
    await add_role_for_dialog(db, msg.chat.id, msg.text)
    await msg.answer("Роль сохранена")
    await state.clear()


@router.message(Command(commands="clear"), flags={"db": True})
async def cmd_clear_dialog(msg: Message, db: AsyncSession):
    """Команда /clear (очистка диалога)"""
    await clear_dialog_context(db, msg.chat.id)
    await msg.answer("Контекст очищен")


@router.message(flags={"db": True})
async def get_request(msg: Message, db: AsyncSession):
    """Запросы для openai. Хендлер ловит все остальные текстовые сообщения.
    Если есть история диалога, добавлеяет ее к запросу и делает запрос в openai"""
    if msg.text is None:
        return
    messages_to_request = await get_messages_to_request(db, msg.chat.id, msg.text)
    response = await response_from_gpt(db, msg.chat.id, messages_to_request)
    await msg.answer(response)
    await msg.answer_voice(await response_audio(response))
