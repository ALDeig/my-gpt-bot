from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.src.services.db.models import ImageForamt, ImageStyle, TTSVoice


kb_settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔊 Голос", callback_data="tts_voice")],
        [InlineKeyboardButton(text="📐 Формат", callback_data="image_format")],
        [InlineKeyboardButton(text="🎨 Стиль", callback_data="image_style")],
    ]
)


def kb_select_setting(
    params: type[TTSVoice | ImageStyle | ImageForamt],
    selected_param: TTSVoice | ImageStyle | ImageForamt | None,
) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for param in params:
        emoji = "✅ " if param == selected_param else ""
        button = [
            InlineKeyboardButton(text=f"{emoji}{param.value}", callback_data=param)
        ]
        inline_keyboard.append(button)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

