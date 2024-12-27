from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.src.dialogs.keyboards.settings import (
    kb_select_model,
    kb_select_setting,
    kb_settings_menu,
)
from app.src.dialogs.states import SettingsState
from app.src.services.db.dao.holder import HolderDao
from app.src.services.openai.enums import ImageFormat, ImageStyle, ModelSource, TTSVoice
from app.src.services.openai.openai_models import get_models_by_source
from app.src.services.texts.settings import SELECT_OPTIONS, settings_text
from app.src.services.user_settings import answer_update_setting, get_open_ai_settings

router = Router()


@router.message(Command("settings"), flags={"dao": True})
async def cmd_settings(msg: Message, dao: HolderDao, state: FSMContext):
    await state.clear()
    settings = await get_open_ai_settings(dao, msg.chat.id)
    await msg.answer(settings_text(settings), reply_markup=kb_settings_menu)


@router.callback_query(
    F.data.startswith("option"),
    F.data.as_("setting_type"),
    flags={"dao": True},
)
async def select_setting_type(
    call: CallbackQuery,
    dao: HolderDao,
    setting_type: str,
    state: FSMContext,
):
    if not isinstance(call.message, Message) or call.data is None:
        return
    await call.answer()
    _, setting_type = setting_type.split(":")
    await state.update_data(setting_type=setting_type)
    settings = await get_open_ai_settings(dao, call.from_user.id)
    match setting_type:
        case "tts_voice":
            kb = kb_select_setting(TTSVoice, settings.tts_voice)
        case "image_style":
            kb = kb_select_setting(ImageStyle, settings.image_style)
        case "image_format":
            kb = kb_select_setting(ImageFormat, settings.image_format)
        case "GPT":
            kb = kb_select_model(await get_models_by_source(dao, ModelSource.GPT))
            await state.update_data(setting_type="gpt_model_id")
        case "DALLE":
            kb = kb_select_model(await get_models_by_source(dao, ModelSource.DALLE))
            await state.update_data(setting_type="dalle_id")
        case _:
            await call.message.answer("Неизвестная команда")
            return
    await call.message.edit_text(SELECT_OPTIONS, reply_markup=kb)
    await state.set_state(SettingsState.options)


@router.callback_query(SettingsState.options, flags={"dao": True})
async def select_tts_voice(call: CallbackQuery, dao: HolderDao, state: FSMContext):
    if call.data is None or not isinstance(call.message, Message):
        return
    await call.answer()
    data = await state.get_data()
    settings = await answer_update_setting(
        dao,
        call.from_user.id,
        data["setting_type"],
        call.data if not call.data.isdigit() else int(call.data),
    )
    await call.message.edit_text(settings_text(settings), reply_markup=kb_settings_menu)
    await state.clear()
