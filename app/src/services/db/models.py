import enum

from sqlalchemy import BigInteger, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.src.services.db.base import Base


class TTSVoice(enum.StrEnum):
    """Голоса."""

    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"
    NOT_SELECT = "not_select"


class ImageForamt(enum.StrEnum):
    """Форматы изображений."""

    SQUARE = "1024x1024"
    LAND = "1792x1024"
    PORT = "1024x1792"


class ImageStyle(enum.StrEnum):
    """Стили изображений."""

    VIVID = "vivid"
    NATURAL = "natural"


class User(Base):
    """Таблица пользователей."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)


class Dialog(Base):
    """Таблица диалогов."""

    __tablename__ = "dialogs"

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    role: Mapped[str]
    content: Mapped[str]


class Settings(Base):
    """Таблица настройок."""

    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    tts_voice: Mapped[TTSVoice] = mapped_column(
        Enum(TTSVoice), default=TTSVoice.NOT_SELECT
    )
    image_style: Mapped[ImageStyle] = mapped_column(
        Enum(ImageStyle), default=ImageStyle.VIVID
    )
    image_format: Mapped[ImageForamt] = mapped_column(
        Enum(ImageForamt), default=ImageForamt.SQUARE
    )


class AIModels(Base):
    """Таблица openai моделей."""

    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    source: Mapped[str] = mapped_column(Text)
    model: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
