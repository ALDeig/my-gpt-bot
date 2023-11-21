from typing import Literal

from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.settings import kb_select_setting, kb_settings_menu
from app.src.services.db import db_requests
from app.src.services.db.tables import ImageForamt, ImageStyle, TTSVoice


async def get_settings_answer(
    session: AsyncSession, user_id: int
) -> tuple[str, InlineKeyboardMarkup]:
    settings = await db_requests.get_settings(session, user_id)
    tts_voice_text = (
        "Не выбран"
        if settings.tts_voice == TTSVoice.NOT_SELECT
        else settings.tts_voice.value
    )
    text = (
        f"🆔 Ваш id: {user_id}\n"
        f"🔊 Голос: {tts_voice_text}\n"
        f"🎨 Стиль: {settings.image_style.value}\n"
        f"📐 Формат: {settings.image_format.value}"
    )
    return text, kb_settings_menu


async def get_answer_setting_type(
    session: AsyncSession,
    user_id: int,
    setting_type: Literal["tts_voice", "image_style", "image_format"],
) -> tuple[str, InlineKeyboardMarkup]:
    settings = await db_requests.get_settings(session, user_id)
    match setting_type:
        case "tts_voice":
            kb = kb_select_setting(TTSVoice, settings.tts_voice)
        case "image_style":
            kb = kb_select_setting(ImageStyle, settings.image_style)
        case _:
            kb = kb_select_setting(ImageForamt, settings.image_format)
    return "Выберите один из вариантов", kb


async def answer_update_setting(
    session: AsyncSession, user_id: int, setting_type: str, value: str
) -> tuple[str, InlineKeyboardMarkup]:
    await db_requests.update_settings(session, user_id, {setting_type: value})
    return await get_settings_answer(session, user_id)
