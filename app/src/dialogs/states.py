from aiogram.fsm.state import State, StatesGroup


class SettingsState(StatesGroup):
    """Состояния для настроек."""

    options = State()


class OpenAiState(StatesGroup):
    """Состояния для OpenAI."""

    role = State()
    image_prompt = State()


class ModelSettingsState(StatesGroup):
    """Состояния для добавления модели."""

    source = State()
    model = State()
    description = State()
    select_model = State()
