import aioboto3

from src.settings import get_settings


async def get_cognito_client():
    settings = get_settings()
    session = aioboto3.Session()

    return session.client(
        "cognito-idp",
        region_name=settings.aws_cognito_region,
        aws_access_key_id=settings.aws_access_key_id.get_secret_value(),
        aws_secret_access_key=settings.aws_secret_access_key.get_secret_value(),
    )


async def login(username: str, password: str, user_repository):
    settings = get_settings()
    client = await get_cognito_client()

    async with client() as client:
        try:
            response_token = await client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password,
                },
                ClientId=settings.aws_cognito_client_id.get_secret_value(),
            )

            if response_token.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
                await client.admin_set_user_password(
                    UserPoolId=settings.aws_cognito_user_pool.get_secret_value(),
                    Username=username,
                    Password=password,
                    Permanent=True,
                )
                response_token = await client.initiate_auth(
                    AuthFlow="USER_PASSWORD_AUTH",
                    AuthParameters={
                        "USERNAME": username,
                        "PASSWORD": password,
                    },
                    ClientId=settings.aws_secret_access_key.get_secret_value(),
                )

            response_user = await client.get_user(AccessToken=response_token["AuthenticationResult"]["AccessToken"])

            user_attributes = {attr["Name"]: attr["Value"] for attr in response_user["UserAttributes"]}

            if not await user_repository.get_by_cognito_id(cognito_id=user_attributes["sub"]):
                await user_repository.create(
                    cognito_id=user_attributes["sub"],
                    username=response_user["Username"],
                    email=user_attributes["email"],
                )

            return (
                response_token["AuthenticationResult"]["AccessToken"],
                response_token["AuthenticationResult"]["RefreshToken"],
            )

        except Exception as e:
            print(e)


async def logout(access_token: str):
    client = await get_cognito_client()

    async with client() as client:
        try:
            await client.global_sign_out(AccessToken=access_token)
        except client.exceptions.NotAuthorizedException:
            pass
