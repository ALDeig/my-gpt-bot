from typing import Literal
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.user_settings import (
    answer_update_setting,
    get_answer_setting_type,
    get_settings_answer,
)


router = Router()


@router.message(Command("settings"), flags={"db": True})
async def cmd_settings(msg: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    text, kb = await get_settings_answer(db, msg.chat.id)
    await msg.answer(text, reply_markup=kb)


@router.callback_query(
    F.data.in_(("tts_voice", "image_format", "image_style")),
    F.data.as_("setting_type"),
    flags={"db": True},
)
async def select_setting_type(
    call: CallbackQuery,
    db: AsyncSession,
    setting_type: Literal["tts_voice", "image_format", "image_style"],
    state: FSMContext,
):
    if call.message is None or call.data is None:
        return
    await call.answer()
    await state.update_data(setting_type=setting_type)
    text, kb = await get_answer_setting_type(db, call.from_user.id, setting_type)
    await call.message.edit_text(text, reply_markup=kb)
    await state.set_state("select_setting_param")


@router.callback_query(StateFilter("select_setting_param"), flags={"db": True})
async def select_tts_voice(call: CallbackQuery, db: AsyncSession, state: FSMContext):
    if call.data is None or call.message is None:
        return
    await call.answer()
    data = await state.get_data()
    text, kb = await answer_update_setting(
        db, call.from_user.id, data["setting_type"], call.data
    )
    await call.message.edit_text(text, reply_markup=kb)
    await state.clear()
