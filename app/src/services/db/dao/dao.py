from app.src.services.db.dao.base_dao import BaseDao
from app.src.services.db.models import Dialog, Settings, User


class UserDao(BaseDao[User]):
    """DAO для работы с пользователями."""

    model = User


class DialogDao(BaseDao[Dialog]):
    """DAO для работы с диалогами."""

    model = Dialog


class SettingDao(BaseDao[Settings]):
    """DAO для работы с настройками."""

    model = Settings
