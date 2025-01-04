from typing import Literal

from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.services.db.base import Base
from app.src.services.openai.enums import (
    ImageFormatType,
    ImageStyleType,
    ModelSource,
    TTSVoiceType,
)


class User(Base):
    """Таблица пользователей."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)


class AIModel(Base):
    """Таблица openai моделей."""

    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    source: Mapped[ModelSource] = mapped_column(Text)
    model: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class Chat(Base):
    """Таблица чатов."""

    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    model_id: Mapped[int] = mapped_column(ForeignKey(AIModel.id, ondelete="CASCADE"))
    type: Mapped[Literal["bot", "app"]] = mapped_column(String(3))

    model: Mapped[AIModel] = relationship(lazy="selectin", init=False)
    messages: Mapped[list["AIChatMessage"]] = relationship(
        back_populates="chat", lazy="selectin", init=False
    )


class AIChatMessage(Base):
    """Таблица сообщений c ИИ."""

    __tablename__ = "ai_chat_messages"

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    role: Mapped[Literal["user", "developer", "assistant"]] = mapped_column(String(9))
    content: Mapped[str] = mapped_column(Text)

    chat: Mapped["Chat"] = relationship(
        back_populates="messages", lazy="selectin", init=False
    )


# class Dialog(Base):
#     """Таблица диалогов."""
#
#     __tablename__ = "dialogs"
#
#     id: Mapped[int] = mapped_column(
#         Integer, init=False, primary_key=True, autoincrement=True
#     )
#     user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
#     model_id: Mapped[int] = mapped_column(ForeignKey(AIModel.id, ondelete="CASCADE"))
#     type: Mapped[Literal["bot", "app"]] = mapped_column(String(3))
#     role: Mapped[Literal["user", "developer"]] = mapped_column(String(9))
#     content: Mapped[str] = mapped_column(Text)
#


class Settings(Base):
    """Таблица настройок."""

    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(ForeignKey(User.id), primary_key=True)
    tts_voice: Mapped[TTSVoiceType | None] = mapped_column(Text, default=None)
    image_style: Mapped[ImageStyleType] = mapped_column(Text, default="vivid")
    image_format: Mapped[ImageFormatType] = mapped_column(Text, default="1024x1024")
    gpt_model_id: Mapped[int | None] = mapped_column(
        ForeignKey("ai_models.id"), default=None
    )
    dalle_id: Mapped[int | None] = mapped_column(
        ForeignKey("ai_models.id"), default=None
    )

    gpt_model: Mapped["AIModel"] = relationship(
        init=False, lazy="selectin", foreign_keys=gpt_model_id
    )
    dalle_model: Mapped["AIModel"] = relationship(
        init=False, lazy="selectin", foreign_keys=dalle_id
    )
