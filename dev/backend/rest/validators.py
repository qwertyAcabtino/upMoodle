from django.core.exceptions import ValidationError
from rest.ERROR_MESSAGE_ID import PASSWORD_LENGTH, NICK_LENGTH


def validate_password(value, lengthMin=8, lengthMax=100, ):
    if len(str(value)) < lengthMin or len(str(value)) > lengthMax:
        raise ValidationError(PASSWORD_LENGTH)


def validate_nick(value, lengthMin=4, lengthMax=20):
    if len(str(value)) < lengthMin or len(str(value)) > lengthMax:
        raise ValidationError(NICK_LENGTH)