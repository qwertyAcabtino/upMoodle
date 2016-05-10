from django.core.exceptions import ValidationError

from upmoodle.models.message.errorMessage import ErrorMessage


def validate_length(value, max_length, min_length=0, code=ErrorMessage.Type.INCORRECT_DATA):
    from upmoodle.models.utils.requestException import RequestExceptionByCode
    if min_length > 0 and len(str(value)) < min_length:
        raise RequestExceptionByCode(code)
    if len(str(value)) > max_length:
        raise RequestExceptionByCode(code)
