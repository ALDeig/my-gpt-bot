import enum
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.services.db.base import Base


class TTSVoice(str, enum.Enum):
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"
    NOT_SELECT = "not_select"


class ImageForamt(str, enum.Enum):
    SQUARE = "1024x1024"
    LAND = "1792x1024"
    PORT = "1024x1792"


class ImageStyle(str, enum.Enum):
    VIVID = "vivid"
    NATURAL = "natural"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)


class Dialog(Base):
    __tablename__ = "dialogs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    role: Mapped[str]
    content: Mapped[str]


class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
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


class Settings2(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    gpt_model_id: Mapped[int] = mapped_column(ForeignKey("gpt_models.id"))
    gpt_model: Mapped["GPTModel"] = relationship()
    tts_voice_id: Mapped[Optional[int]] = mapped_column(ForeignKey("voices.id"))
    tts_voice: Mapped[Optional["Voice"]] = relationship()
    image_style_id: Mapped[Optional[int]] = mapped_column(ForeignKey("image_styles.id"))
    image_style: Mapped[Optional["ImageStyle"]] = relationship()
    image_format_id: Mapped[Optional[int]] = mapped_column(ForeignKey("image_format.id"))
    image_format: Mapped[Optional["ImageForamt"]] = relationship()


class Voice(Base):
    __tablename__ = "voices"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]
    verbose_name: Mapped[str]
    desctiption: Mapped[str] = mapped_column(String, nullable=True)


class ImageStyle(Base):
    __tablename__ = "image_styles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]
    verbose_name: Mapped[str]
    desctiption: Mapped[str] = mapped_column(String, nullable=True)


class ImageFormat(Base):
    __tablename__ = "image_formats"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]
    verbose_name: Mapped[str]
    desctiption: Mapped[str] = mapped_column(String, nullable=True)


class GPTModel(Base):
    __tablename__ = "gpt_models"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]
    verbose_name: Mapped[str]
    desctiption: Mapped[str] = mapped_column(String, nullable=True)

