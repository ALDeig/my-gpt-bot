from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.settings import settings


def web_app_keyboard(user_id: int):
    kb = ReplyKeyboardBuilder()
    url_applications = f"{settings.BASE_URL}?user_id={user_id}"
    kb.button(text="🌐 WEB чаты", web_app=WebAppInfo(url=url_applications))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
