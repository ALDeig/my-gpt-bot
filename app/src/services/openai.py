import openai

from app.settings import settings 


openai.api_key = settings.openai_api_key


async def get_response_from_gpt(messages: list[dict[str, str]]) -> str:
    """Делает запрос в openai и возвращает ответ. Модель используется GPT-4"""
    completion = await openai.ChatCompletion.acreate(
        model="gpt-4", messages=messages, temperature=0.5
    )
    response_content = completion.choices[0].message.content  # type: ignore
    return response_content
