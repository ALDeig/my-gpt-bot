from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.src.dialogs.states import OpenAiState
from app.src.services.db.dao.holder import HolderDao
from app.src.services.dialogs import (
    add_role_for_dialog,
    clear_dialog_context,
    generate_image,
    response_audio,
    response_from_gpt,
)
from app.src.services.texts.open_ai import (
    CONTEXT_CLEAR,
    GET_ROLE,
    IMAGE_ERROR,
    IMAGE_PROMPT,
    ROLE_SAVED,
    STATUS_MESSAGE,
)

router = Router()


@router.message(Command(commands="add_role"))
async def cmd_add_role(msg: Message, state: FSMContext):
    """Хендлер на команду /add_role (добавить роль). Устанавливает состояние для
    добавления роли.
    """
    await msg.answer(GET_ROLE)
    await state.set_state(OpenAiState.role)


@router.message(OpenAiState.role, flags={"dao": True})
async def get_role(msg: Message, dao: HolderDao, state: FSMContext):
    """Сообщение с ролью. Сохраняет роль."""
    if msg.text is None:
        return
    await add_role_for_dialog(dao, msg.chat.id, msg.text)
    await msg.answer(ROLE_SAVED)
    await state.clear()


@router.message(Command(commands="clear"), flags={"dao": True})
async def cmd_clear_dialog(msg: Message, dao: HolderDao):
    """Команда /clear (очистка диалога)."""
    await clear_dialog_context(dao, msg.chat.id)
    await msg.answer(CONTEXT_CLEAR)


@router.message(Command(commands="image"))
async def cmd_image(msg: Message, state: FSMContext):
    await msg.answer(IMAGE_PROMPT)
    await state.set_state(OpenAiState.image_prompt)


@router.message(StateFilter(OpenAiState.image_prompt), flags={"dao": True})
async def get_image_promts(msg: Message, dao: HolderDao, state: FSMContext):
    await state.clear()
    if msg.text is None:
        return
    status_message = await msg.answer(STATUS_MESSAGE)
    response = await generate_image(dao, msg.chat.id, msg.text)
    await status_message.delete()
    if response is None:
        await msg.answer(IMAGE_ERROR)
        return
    await msg.answer_document(response)


@router.message(flags={"dao": True})
async def get_request(msg: Message, dao: HolderDao):
    """Запросы для openai. Хендлер ловит все остальные текстовые сообщения.
    Если есть история диалога, добавлеяет ее к запросу и делает запрос в openai.
    """
    if msg.text is None:
        return
    status_message = await msg.answer(STATUS_MESSAGE)
    response = await response_from_gpt(dao, msg.chat.id, msg.text)
    await status_message.delete()
    await msg.answer(response, parse_mode="MarkdownV2")
    audio = await response_audio(dao, msg.chat.id, response)
    if audio is not None:
        await msg.answer_voice(audio)
