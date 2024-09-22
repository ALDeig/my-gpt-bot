from app.src.services.db.models import Settings, TTSVoice

SELECT_OPTIONS = "Выберите один из вариантов"


def settings_text(settings: Settings) -> str:
    tts_voice_text = (
        "Не выбран"
        if settings.tts_voice == TTSVoice.NOT_SELECT
        else settings.tts_voice.value
    )
    return (
        f"🆔 Ваш id: {settings.id}\n"
        f"🔊 Голос: {tts_voice_text}\n"
        f"🎨 Стиль: {settings.image_style.value}\n"
        f"📐 Формат: {settings.image_format.value}"
    )
