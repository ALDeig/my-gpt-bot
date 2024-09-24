from aiogram.fsm.state import State, StatesGroup


class SettingsState(StatesGroup):
    """Состояния для настроек."""

    options = State()


class OpenAiState(StatesGroup):
    """Состояния для OpenAI."""

    role = State()
    image_prompt = State()
