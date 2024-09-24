import enum
from typing import Literal


class TTSVoice(enum.StrEnum):
    """Голоса."""

    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"


class ImageFormat(enum.StrEnum):
    """Форматы изображений."""

    SQUARE = "1024x1024"
    LAND = "1792x1024"
    PORT = "1024x1792"


class ImageStyle(enum.StrEnum):
    """Стили изображений."""

    VIVID = "vivid"
    NATURAL = "natural"


type TTSVoiceType = Literal[
    "alloy",
    "echo",
    "fable",
    "onyx",
    "nova",
    "shimmer",
]

type ImageFormatType = Literal[
    "1024x1024",
    "1792x1024",
    "1024x1792",
]

type ImageStyleType = Literal[
    "vivid",
    "natural",
]
