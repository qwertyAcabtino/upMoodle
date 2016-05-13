from upmoodle.models import ErrorMessage

from backend.settings import SESSION_COOKIE_NAME
from upmoodle.models.utils.newJsonResponse import NewJsonResponse


class MessageBasedException(Exception):

    def __str__(self):
        return repr(self)

    def __init__(self, **kwargs):
        self.message_id = kwargs.get('message_id', ErrorMessage.Type.INCORRECT_DATA)
        exception = kwargs.get('exception', None)
        if exception:
            self.__set_stack_trace(kwargs.get('exception'))

    def __set_stack_trace(self, exception):
        if len(exception.message):
            self.stack_trace = exception.message
        elif hasattr(exception, 'messages') and len(exception.messages):
            self.stack_trace = '\n. '.join(exception.messages)

    def get_json_response(self):
        response = NewJsonResponse(message_id=self.message_id, exception=self)
        response.set_cookie(SESSION_COOKIE_NAME)
        return response
