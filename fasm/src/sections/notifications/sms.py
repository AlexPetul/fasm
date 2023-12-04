import aioboto3

from src.settings import get_settings


async def send_sms(username: str, questions_count: int):
    settings = get_settings()
    session = aioboto3.Session()

    async with session.client(
        "sns",
        region_name=settings.aws_cognito_region,
        aws_access_key_id=settings.aws_access_key_id.get_secret_value(),
        aws_secret_access_key=settings.aws_secret_access_key.get_secret_value(),
    ) as client:
        client.publish(
            TopicArn="arn:aws:sns:us-east-1:353586219743:test",
            PhoneNumber=settings.reviewer_phone,
            Message=f"You have received {questions_count} new questions from {username} for review!",
        )
