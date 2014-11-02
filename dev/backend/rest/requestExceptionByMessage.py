from rest.JSONResponse import JSONResponse
from rest.exceptions import INCORRECT_DATA
from rest.models import ErrorMessage
from rest.serializers import ErrorMessageSerializer


class RequestExceptionByMessage(Exception):
    jsonResponse = None

    def __init__(self, validationError):

        try:
            code = int(validationError.messages[0])
            error = ErrorMessage.objects.get(pk=code)
        except ValueError as v:
            error = ErrorMessage.objects.get(pk=INCORRECT_DATA)
            if len(validationError.message):
                error.error += ". "+validationError.message
            else:
                error.error += ". "+' '.join(validationError.messages)
        finally:
            serializer = ErrorMessageSerializer(error, many=False)
            self.jsonResponse = JSONResponse(serializer.data, status=400)

    def __str__(self):
        return repr(self)


class RequestExceptionByCode(Exception):
    jsonResponse = None

    def __init__(self, code):
        error = ErrorMessage.objects.get(pk=code)
        serializer = ErrorMessageSerializer(error, many=False)
        self.jsonResponse = JSONResponse(serializer.data, status=400)

    def __str__(self):
        return repr(self)
