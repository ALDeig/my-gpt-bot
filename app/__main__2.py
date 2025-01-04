import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.commands import set_commands
from app.settings import settings
from app.src.dialogs.handlers import admin, model_settings, openai, user, user_settings
from app.src.middleware.db import DbSessionMiddleware

logger = logging.getLogger(__name__)


def include_routers(dp: Dispatcher):
    """Регистрация хендлеров."""
    dp.include_routers(
        user_settings.router,
        admin.router,
        model_settings.router,
        openai.router,
        user.router,
    )


def include_filters(admins: list[int], dp: Dispatcher):
    """Регистрация фильтров для хендлеров."""
    dp.message.filter(F.chat.type == "private")
    admin.router.message.filter(F.chat.id.in_(admins))
    admin.router.callback_query.filter(F.chat.id.in_(admins))
    model_settings.router.message.filter(F.chat.id.in_(admins))
    model_settings.router.callback_query.filter(F.chat.id.in_(admins))
    openai.router.message.filter(F.chat.id.in_(admins))
    openai.router.callback_query.filter(F.chat.id.in_(admins))


async def main():
    bot = Bot(
        token=settings.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация фильтров
    include_filters(settings.ADMINS, dp)

    # Регистрация middlewares
    dp.message.middleware(DbSessionMiddleware())
    dp.callback_query.middleware(DbSessionMiddleware())

    # Регистрация хендлеров
    include_routers(dp)

    # Установка команд для бота
    await set_commands(bot, settings.ADMINS)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        logger.warning("Bot starting...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Bot stopping...")
