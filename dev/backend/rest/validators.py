from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from rest.MESSAGES_ID import PASSWORD_LENGTH, NICK_LENGTH, EMAIL_EMPTY


def validate_password(value, lengthMin=8, lengthMax=100, ):
    if len(str(value)) < lengthMin or len(str(value)) > lengthMax:
        raise ValidationError(PASSWORD_LENGTH)


def validate_nick(value, lengthMin=4, lengthMax=20):
    if len(str(value)) < lengthMin or len(str(value)) > lengthMax:
        raise ValidationError(NICK_LENGTH)


def validate_email(value):
    if len(value) == 0:
        raise ValidationError(EMAIL_EMPTY)
    else:
        emailValidator = EmailValidator()
    # TODO. Email is upm.es type