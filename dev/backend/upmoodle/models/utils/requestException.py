from backend.settings import SESSION_COOKIE_NAME
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.utils.jsonResponse import JsonResponse


class RequestException(Exception):
    jsonResponse = None

    def __str__(self):
        return repr(self)