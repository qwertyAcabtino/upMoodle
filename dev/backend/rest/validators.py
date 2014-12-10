from django.core.exceptions import ValidationError
from rest.MESSAGES_ID import INCORRECT_DATA


def validate_length(value, lengthMax, lengthMin=0, code=INCORRECT_DATA):
    if lengthMin > 0 and len(str(value)) < lengthMin:
        raise ValidationError(code)
    if len(str(value)) > lengthMax:
        raise ValidationError(code)
