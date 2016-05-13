from upmoodle.models.exceptions.messageBasedException import MessageBasedException
from upmoodle.models.message.errorMessage import ErrorMessage


def validate_length(value, max_length, min_length=0, code=ErrorMessage.Type.INCORRECT_DATA):
    if min_length > 0 and len(str(value)) < min_length:
        raise MessageBasedException(message_id=code)
    if len(str(value)) > max_length:
        raise MessageBasedException(message_id=code)
