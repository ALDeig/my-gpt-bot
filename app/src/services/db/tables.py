from enum import Enum
from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.src.services.db.base import Base


class TTSVoice(str, Enum):
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"
    NOT_SELECT = "not_select"


class ImageForamt(str, Enum):
    SQUARE = "1024x1024"
    LAND = "1792x1024"
    PORT = "1024x1792"


class ImageStyle(str, Enum):
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
    tts_voice: Mapped[TTSVoice] = mapped_column(String, default=TTSVoice.NOT_SELECT)
    image_style: Mapped[ImageStyle] = mapped_column(String, default=ImageStyle.VIVID)
    image_format: Mapped[ImageForamt] = mapped_column(String, default=ImageForamt.SQUARE)
