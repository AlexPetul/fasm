from rest_framework import status
from rest_framework.exceptions import APIException


class CognitoException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class CognitoCredentialsException(CognitoException):
    status_code = status.HTTP_400_BAD_REQUEST
