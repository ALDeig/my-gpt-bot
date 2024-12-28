import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

logger = logging.getLogger(__name__)

USER_COMMANDS = [BotCommand(command="start", description="В начало")]
ADMIN_COMMANDS = [
    BotCommand(command="start", description="В начало"),
    BotCommand(command="image", description="Сгенерировать изображение"),
    BotCommand(command="settings", description="Настройки"),
    BotCommand(command="add_role", description="Добавить роль"),
    BotCommand(command="clear", description="Очистить контекст"),
    BotCommand(command="model", description="Настройки моделей"),
]


async def set_commands(bot: Bot, admins: list[int]):
    """Установка команд для пользователей и администратора."""
    await bot.set_my_commands(commands=USER_COMMANDS, scope=BotCommandScopeDefault())
    for admin_id in admins:
        try:
            await bot.set_my_commands(
                commands=ADMIN_COMMANDS,
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
        except TelegramBadRequest:  # noqa: PERF203
            logger.warning("Can't set commands to admin with ID %s", admin_id)
