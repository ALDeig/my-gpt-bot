import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault


async def set_commands(bot: Bot, admins: list[int]):
    """Установка команд для пользователей и администратора."""
    user_commands = [BotCommand(command="start", description="В начало")]
    await bot.set_my_commands(commands=user_commands, scope=BotCommandScopeDefault())
    admin_commands = [
        BotCommand(command="start", description="В начало"),
        BotCommand(command="image", description="Сгенерировать изображение"),
        BotCommand(command="settings", description="Настройки"),
        BotCommand(command="add_role", description="Добавить роль"),
        BotCommand(command="clear", description="Очистить контекст"),
    ]
    for admin_id in admins:
        try:
            await bot.set_my_commands(
                commands=admin_commands,
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
        except TelegramBadRequest:
            logging.warning("Can't set commands to admin with ID %s", admin_id)
