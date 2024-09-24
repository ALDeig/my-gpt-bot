from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.src.services.db.base import Base
from app.src.services.openai.enums import ImageFormatType, ImageStyleType, TTSVoiceType


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

    id: Mapped[int] = mapped_column(ForeignKey(User.id), primary_key=True)
    tts_voice: Mapped[TTSVoiceType | None] = mapped_column(Text, default=None)
    image_style: Mapped[ImageStyleType] = mapped_column(Text, default="vivid")
    image_format: Mapped[ImageFormatType] = mapped_column(Text, default="1024x1024")


class AIModels(Base):
    """Таблица openai моделей."""

    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    source: Mapped[str] = mapped_column(Text)
    model: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
