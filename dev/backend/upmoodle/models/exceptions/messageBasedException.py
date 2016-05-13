from upmoodle.models import ErrorMessage

class MessageBasedException(Exception):

    stack_trace = ''

    def __str__(self):
        return repr(self)

    def __init__(self, **kwargs):
        self.message_id = kwargs.get('message_id', ErrorMessage.Type.INCORRECT_DATA)
        self.exception = kwargs.get('exception', None)
        if self.exception:
            self.__set_stack_trace(kwargs.get('exception'))

    def __set_stack_trace(self, exception):
        if len(exception.message):
            self.stack_trace = ". " + exception.message
        elif hasattr(exception, 'messages') and len(exception.messages):
            self.stack_trace = ". " + "  ".join(exception.messages)