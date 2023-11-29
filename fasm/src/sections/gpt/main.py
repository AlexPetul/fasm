import json

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key="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")


async def ask(section: str, question_type: str) -> dict:
    prompt = (
        f"As an expert in colloquial Persian, generate random {question_type} in English on this topic: {section}."
        "The answer should offer uniqueness."
        "Display an answer as dictionary with double quotes with two keys: question and answer,"
        f"where question is an english {question_type} and answer is the translation of {question_type} in Finglish."
    )

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=200,
    )

    return json.loads(completion.choices[0].message.content)
