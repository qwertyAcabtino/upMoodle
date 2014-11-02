from django.core.exceptions import ValidationError
from rest.exceptions import PASSWORD_LENGTH, NICK_LENGTH


def validate_password(value, length=8):
    if len(str(value)) < length:
        raise ValidationError(PASSWORD_LENGTH)


def validate_nick(value, length=4):
    if len(str(value)) < length:
        raise ValidationError(NICK_LENGTH)