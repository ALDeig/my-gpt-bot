from app.src.services.db.dao.holder import HolderDao


async def save_user(dao: HolderDao, user_id: int, name: str, username: str | None):
    """Сохранение пользователя в базу данных. Функция вызывается при вводе команды
    start.
    """
    await dao.user.insert_or_update(
        "id", {"name", "username"}, id=user_id, name=name, username=username
    )
