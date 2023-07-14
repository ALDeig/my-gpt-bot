import openai

from app.configreader import config


openai.api_key = config.openai_api_key


async def get_response_from_gpt(messages: list[dict[str, str]]) -> str:
    completion = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    response_content = completion.choices[0].message.content
    return response_content

