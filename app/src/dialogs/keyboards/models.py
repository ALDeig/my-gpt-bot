from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.src.services.db.models import AIModel


def kb_select_model(models: Sequence[AIModel]) -> InlineKeyboardMarkup:
    """Клавиатура для выбора модели."""
    builder = InlineKeyboardBuilder()
    for model in models:
        builder.row(InlineKeyboardButton(text=model.model, callback_data=str(model.id)))
    return builder.as_markup()
