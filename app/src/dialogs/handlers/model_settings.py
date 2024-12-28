from typing import cast

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.src.dialogs.keyboards.admin import kb_model_settings, kb_select_source
from app.src.dialogs.keyboards.models import kb_select_model
from app.src.dialogs.states import ModelSettingsState
from app.src.services.admin import (
    add_model,
    delete_model,
    get_model_sources,
    get_models,
)
from app.src.services.db.dao.holder import HolderDao
from app.src.services.texts.admin import (
    ADD_DESCRIPTION_MODEL,
    ADD_MODEL,
    ADD_SOURCE,
    DONE,
    MODEL_SETTINGS,
    SELECT_MODEL,
    SELECT_SOURCE,
)

router = Router()


@router.message(Command("model"))
async def cmd_model(msg: Message, state: FSMContext):
    """Хендлер на команду /model. Выводит меню работы с моделями."""
    await state.clear()
    await msg.answer(MODEL_SETTINGS, reply_markup=kb_model_settings())


@router.callback_query(F.data == "add_model", F.message.as_("msg"))
async def btn_add_model(call: CallbackQuery, msg: Message, state: FSMContext):
    """Хендлер на команду /add_model. Выводит меню работы с моделями."""
    await call.answer()
    sources = get_model_sources()
    if sources:
        kb = kb_select_source(sources)
        text = SELECT_SOURCE
    else:
        kb = None
        text = ADD_SOURCE
    await msg.edit_text(text, reply_markup=kb)
    await state.set_state(ModelSettingsState.source)


@router.message(ModelSettingsState.source)
async def insert_source(msg: Message, state: FSMContext):
    """Хендлер на ввод источника."""
    await state.update_data(source=msg.text)
    await msg.answer(ADD_MODEL)
    await state.set_state(ModelSettingsState.model)


@router.callback_query(ModelSettingsState.source, F.message.as_("msg"))
async def select_source(call: CallbackQuery, msg: Message, state: FSMContext):
    """Хендлер на ввод источника."""
    await call.answer()
    await state.update_data(source=call.data)
    await msg.answer(ADD_MODEL)
    await state.set_state(ModelSettingsState.model)


@router.message(ModelSettingsState.model)
async def get_model(msg: Message, state: FSMContext):
    """Хендлер на ввод названия модели."""
    await state.update_data(model=msg.text)
    await msg.answer(ADD_DESCRIPTION_MODEL)
    await state.set_state(ModelSettingsState.description)


@router.message(ModelSettingsState.description, flags={"dao": True})
async def get_description(msg: Message, dao: HolderDao, state: FSMContext):
    """Хендлер на ввод описания модели."""
    data = await state.get_data()
    await add_model(dao=dao, **data, description=cast("str", msg.text))
    await msg.answer(DONE)
    await state.clear()


@router.callback_query(
    F.data == "delete_model", F.message.as_("msg"), flags={"dao": True}
)
async def btn_delete_model(
    call: CallbackQuery, msg: Message, dao: HolderDao, state: FSMContext
):
    """Хендлер на кнопку удаления модели."""
    await call.answer()
    models = await get_models(dao)
    await msg.edit_text(SELECT_MODEL, reply_markup=kb_select_model(models))
    await state.set_state(ModelSettingsState.select_model)


@router.callback_query(
    ModelSettingsState.select_model, F.message.as_("msg"), flags={"dao": True}
)
async def select_model(
    call: CallbackQuery, msg: Message, dao: HolderDao, state: FSMContext
):
    """Хендлер на выбор модели."""
    await call.answer()
    await state.clear()
    await delete_model(dao, int(cast("str", call.data)))
    await msg.edit_text(DONE)
