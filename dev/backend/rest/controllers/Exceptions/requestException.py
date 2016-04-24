from backend.settings import SESSION_COOKIE_NAME
from rest.JSONResponse import JSONResponse
from rest.models.message.errorMessage import ErrorMessage as errorMessage, ErrorMessageType
from rest.orm.serializers import ErrorMessageSerializer


class RequestException(Exception):
    jsonResponse = None

    def __init__(self, error_message):
        serializer = ErrorMessageSerializer(error_message, many=False)
        self.jsonResponse = JSONResponse(serializer.data, status=error_message.http_code)
        self.jsonResponse.set_cookie(SESSION_COOKIE_NAME)

    def __str__(self):
        return repr(self)


class RequestExceptionByMessage(RequestException):
    def __init__(self, validation_error):

        try:
            code = int(validation_error.messages[0])
            error = errorMessage.objects.get(pk=code)
            super(RequestExceptionByMessage, self).__init__(error)
        except ValueError as v:
            error = errorMessage.objects.get(pk=ErrorMessageType.INCORRECT_DATA.value)
            if len(validation_error.message):
                error.error += ". " + validation_error.message
            else:
                error.error += ". " + '\n. '.join(validation_error.messages)
            super(RequestExceptionByMessage, self).__init__(error)


class RequestExceptionByCode(RequestException):
    def __init__(self, code):
        error = errorMessage.objects.get(pk=code.value)
        super(RequestExceptionByCode, self).__init__(error)
