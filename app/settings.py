import logging.config

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    TELEGRAM_TOKEN: str
    ADMINS: list[int]
    OPENAI_API_KEY: str
    SQLITE_DSN: str
    LOG_LEVEL: str


settings = Settings()  # type: ignore[reportCallIssue]

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": {
            "format": "[%(asctime)s] [%(levelname)-7s] [%(name)s] > %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default_formatter",
            "filename": "logs/app.log",
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 3
        },

    },
    "loggers": {
        "root": {
            "handlers": ["stream_handler", "file_handler"],
            "level": settings.LOG_LEVEL,
            "propagate": True,
        },
        "httpx": {
            "handlers": ["stream_handler"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}


logging.config.dictConfig(LOGGING_CONFIG)
