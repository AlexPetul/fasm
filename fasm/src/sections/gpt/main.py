import json

from openai import AsyncOpenAI

from src.settings import get_settings

settings = get_settings()

client = AsyncOpenAI(api_key=settings.openai_api_key.get_secret_value())


async def ask(section: str, question_type: str, hint: str = None) -> dict:
    prompt = (
        f"As an expert in Persian, generate random simple {question_type} in English on this topic: {hint or section}."
        "The answer should offer uniqueness and have informal form."
        "Display an answer as dictionary with double quotes with two keys: question and answer,"
        f"where question is an english {question_type} and answer is the translation of {question_type} in Finglish."
    )

    completion = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=200,
    )

    return json.loads(completion.choices[0].message.content)
