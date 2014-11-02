from rest.JSONResponse import JSONResponse
from rest.models import ErrorMessage
from rest.serializers import ErrorMessageSerializer


class RequestException(Exception):
    jsonResponse = None
    def __init__(self, code):
        error = ErrorMessage()
        error.error = ErrorMessage.objects.get(pk=code)
        serializer = ErrorMessageSerializer(error, many=False)
        self.jsonResponse = JSONResponse(serializer.data, status=400)

    def __str__(self):
        return repr(self)