from backend.settings import SESSION_COOKIE_NAME
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.utils.jsonResponse import JsonResponse


class RequestException(Exception):
    jsonResponse = None

    def __str__(self):
        return repr(self)


class RequestExceptionByCode(RequestException):

    def __init__(self, code):
        self.jsonResponse = JsonResponse(message_id=code)
        self.jsonResponse.set_cookie(SESSION_COOKIE_NAME)


class RequestExceptionByMessage(RequestException):

    def __init__(self, validation_error, **kwargs):
        try:
            code = int(validation_error.messages[0])
            error_type_name = ErrorMessage.Type._member_names_[code - 1]
            error_type = ErrorMessage.Type.__members__[error_type_name]
            self.jsonResponse = JsonResponse(message_id=error_type)
            self.jsonResponse.set_cookie(SESSION_COOKIE_NAME)
        except ValueError:
            if len(validation_error.message):
                kwargs['stack_trace'] = validation_error.message
            else:
                kwargs['stack_trace'] = '\n. '.join(validation_error.messages)
            self.jsonResponse = JsonResponse(message_id=ErrorMessage.Type.INCORRECT_DATA, **kwargs)
            self.jsonResponse.set_cookie(SESSION_COOKIE_NAME)

