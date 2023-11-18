from typing import Literal
from openai import AsyncOpenAI

from app.settings import settings


client = AsyncOpenAI(api_key=settings.openai_api_key)


async def get_response_from_gpt(messages: list[dict[str, str]]) -> str | None:
    """Делает запрос в openai и возвращает ответ. Модель используется GPT-4"""
    completion = await client.chat.completions.create(
        model="gpt-4", messages=messages, temperature=0.5  # type: ignore
    )
    response_content = completion.choices[0].message.content
    return response_content


async def text_to_speech(text: str) -> bytes:
    """Отправляет в openai запрос с текстом и получает аудио контент этого текста"""
    response = await client.audio.speech.create(
        model="tts-1-hd", voice="nova", input=text
    )
    return response.content


async def get_image_from_gpt(
    prompt: str,
    size: Literal["1024x1024", "1792x1024", "1024x1792"],
    style: Literal["vivid", "natural"],
) -> str | None:
    """Отправляет запрос в openai с описанием 
    изображения и получает ссылку на изображение"""
    response = await client.images.generate(
        prompt=prompt, model="dall-e-3", quality="hd", size=size, style=style
    )
    return response.data[0].url
