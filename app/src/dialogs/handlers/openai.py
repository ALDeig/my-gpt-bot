from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.dialogs import (
    add_role_for_dialog,
    clear_dialog_context,
    generate_image,
    response_audio,
    response_from_gpt,
)


router = Router()


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


@router.message(Command(commands="image"))
async def cmd_image(msg: Message, state: FSMContext):
    await msg.answer("Введите запрос для генерации изображения")
    await state.set_state("get_image_promts")


@router.message(StateFilter("get_image_promts"), flags={"db": True})
async def get_image_promts(msg: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    if msg.text is None: return
    response = await generate_image(db, msg.chat.id, msg.text)
    if response is None:
        await msg.answer("Не удалось сгенерировать изображение")
        return
    await msg.answer_document(response)


@router.message(flags={"db": True})
async def get_request(msg: Message, db: AsyncSession):
    """Запросы для openai. Хендлер ловит все остальные текстовые сообщения.
    Если есть история диалога, добавлеяет ее к запросу и делает запрос в openai"""
    if msg.text is None:
        return
    status_message = await msg.answer("⠀\n✅ Запрос отправлен\n⠀")
    response = await response_from_gpt(db, msg.chat.id, msg.text)
    await status_message.delete()
    await msg.answer(response)
    audio = await response_audio(db, msg.chat.id, response)
    if audio is not None:
        await msg.answer_voice(audio)
