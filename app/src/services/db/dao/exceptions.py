class DaoNotFoundError(Exception):
    """Ошибка если в классе HolderDAO не найден DAO."""


class AddModelError(Exception):
    """Ошибка при добавлении модели в базу данных."""
