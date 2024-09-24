from app.src.services.db.models import Settings

SELECT_OPTIONS = "Выберите один из вариантов"


def settings_text(settings: Settings) -> str:
    tts_voice_text = (
        "Не выбран"
        if settings.tts_voice is None
        else settings.tts_voice
    )
    return (
        f"🆔 Ваш id: {settings.id}\n"
        f"🔊 Голос: {tts_voice_text}\n"
        f"🎨 Стиль: {settings.image_style}\n"
        f"📐 Формат: {settings.image_format}"
    )
