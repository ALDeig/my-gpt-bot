from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def kb_model_settings() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить модель", callback_data="add_model")],
            [InlineKeyboardButton(text="Удалить модель", callback_data="delete_model")],
        ]
    )


def kb_select_source(sources: Sequence[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for source in sources:
        builder.row(InlineKeyboardButton(text=source, callback_data=source))
    return builder.as_markup()
