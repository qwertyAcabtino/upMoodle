from rest.MESSAGES_ID import INCORRECT_DATA
from rest.JSONResponse import JSONResponse
from rest.models import ErrorMessage
from rest.orm.serializers import ErrorMessageSerializer


class RequestException(Exception):
    jsonResponse = None

    def __init__(self, errorMessage):
        serializer = ErrorMessageSerializer(errorMessage, many=False)
        self.jsonResponse = JSONResponse(serializer.data, status=400)

    def __str__(self):
        return repr(self)


class RequestExceptionByMessage(RequestException):

    def __init__(self, validationError):

        try:
            code = int(validationError.messages[0])
            error = ErrorMessage.objects.get(pk=code)
            super(RequestExceptionByMessage, self).__init__(error)
        except ValueError as v:
            error = ErrorMessage.objects.get(pk=INCORRECT_DATA)
            if len(validationError.message):
                error.error += ". "+validationError.message
            else:
                error.error += ". "+'\n. '.join(validationError.messages)
            super(RequestExceptionByMessage, self).__init__(error)


class RequestExceptionByCode(RequestException):

    def __init__(self, code):
        error = ErrorMessage.objects.get(pk=code)
        super(RequestExceptionByCode, self).__init__(error)
