from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.src.services.openai.enums import (
    ImageFormat,
    ImageFormatType,
    ImageStyle,
    ImageStyleType,
    TTSVoice,
    TTSVoiceType,
)

kb_settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔊 Голос", callback_data="tts_voice")],
        [InlineKeyboardButton(text="📐 Формат", callback_data="image_format")],
        [InlineKeyboardButton(text="🎨 Стиль", callback_data="image_style")],
    ]
)


def kb_select_setting(
    params: type[TTSVoice | ImageStyle | ImageFormat],
    selected_param: TTSVoiceType | ImageStyleType | ImageFormatType | None,
) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for param in params:
        emoji = "✅ " if param == selected_param else ""
        button = [
            InlineKeyboardButton(text=f"{emoji}{param.value}", callback_data=param)
        ]
        inline_keyboard.append(button)
    if params is TTSVoice:
        emoji = "✅ " if selected_param is None else ""
        inline_keyboard.append(
            [InlineKeyboardButton(text=f"{emoji}Не выбран", callback_data="not_select")]
        )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
