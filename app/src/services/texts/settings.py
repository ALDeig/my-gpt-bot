from app.src.services.db.models import Settings

SELECT_OPTIONS = "Выберите один из вариантов"


def settings_text(settings: Settings) -> str:
    tts_voice_text = "Не выбран" if settings.tts_voice is None else settings.tts_voice
    gpt_model_text = "Не выбран" if not settings.gpt_model else settings.gpt_model.model
    dalle_model_text = (
        "Не выбран" if not settings.dalle_model else settings.dalle_model.model
    )
    return (
        f"🆔 Ваш id: {settings.id}\n"
        f"🎛 Модель GPT: {gpt_model_text}\n"
        f"🎛 Модель DALL-E: {dalle_model_text}\n"
        f"🔊 Голос: {tts_voice_text}\n"
        f"🎨 Стиль: {settings.image_style}\n"
        f"📐 Формат: {settings.image_format}"
    )
