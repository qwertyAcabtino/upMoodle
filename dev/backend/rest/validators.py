from django.core.exceptions import ValidationError

from rest.models.message.errorMessage import ErrorMessage


def validate_length(value, lengthMax, lengthMin=0, code=ErrorMessage.Type.INCORRECT_DATA):
    if lengthMin > 0 and len(str(value)) < lengthMin:
        raise ValidationError(code.value)
    if len(str(value)) > lengthMax:
        raise ValidationError(code.value)
