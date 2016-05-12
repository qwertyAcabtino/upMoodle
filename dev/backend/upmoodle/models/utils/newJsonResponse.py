from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from upmoodle.models import OkMessage, ErrorMessage


class NewJsonResponse(HttpResponse):
    MEDIA_TYPE = 'application/json'

    response_content = dict()
    http_code = 200

    def __init__(self, body=None, message_id=None, exception=None):

        self._set_response_body(body)
        self._set_response_message(message_id=message_id, exception=exception)
        content = JSONRenderer().render(self.response_content)
        super(NewJsonResponse, self).__init__(content, status=self.http_code)
        self._ensure_headers()

    def _set_response_message(self, message_id=None, exception=None):
        global response_message
        message_key = None

        if message_id and type(message_id.get()) == OkMessage:
            response_message = OkMessage.objects.get(pk=message_id.value).json
            message_key = 'message'

        elif message_id and type(message_id.get()) == ErrorMessage:
            response_message = ErrorMessage.objects.get(pk=message_id.value).json
            message_key = 'error'

        elif exception:
            response_message = ErrorMessage.objects.get(pk=exception.message_id.value).json
            message_key = 'error'
            if hasattr(exception, 'stack_trace'):
                self.response_content[message_key]['text'] += ". " + exception.stack_trace

        if message_key:
            self.http_code = response_message['http_code']
            self.response_content[message_key] = response_message

    def _set_response_body(self, body):
        if body is not None:
            try:
                self.response_content.__setitem__('id', body.id)
                # self.response_content.__setitem__('data', dict())
                # self.response_content.get('data').__setitem__('id', body.id)
            except AttributeError:
                self.response_content = body
                # self.response_content.__setitem__('data', body)

    def _ensure_headers(self):
        self['Content-Type'] = self.MEDIA_TYPE
        self['Access-Control-Expose-Headers'] = '*'
        self['Access-Control-Allow-Credentials'] = 'true'


class ErrorMessageException(HttpResponse):
    MEDIA_TYPE = 'application/json'

    response_content = dict()
    http_code = 200

    def __init__(self, message_id=None, exception=None):

        self._set_response_message(message_id=message_id, exception=exception)
        content = JSONRenderer().render(self.response_content)
        super(ErrorMessageException, self).__init__(content, status=self.http_code)
        self._ensure_headers()

    def _set_response_message(self, message_id=None, exception=None):
        global response_message
        message_key = None

        if message_id and type(message_id.get()) == OkMessage:
            response_message = OkMessage.objects.get(pk=message_id.value).json
            message_key = 'message'

        elif message_id and type(message_id.get()) == ErrorMessage:
            response_message = ErrorMessage.objects.get(pk=message_id.value).json
            message_key = 'error'

        elif exception:
            response_message = ErrorMessage.objects.get(pk=exception.message_id.value).json
            message_key = 'error'
            if exception.stack_trace:
                self.response_content[message_key]['text'] += ". " + exception.stack_trace

        if message_key:
            self.http_code = response_message['http_code']
            self.response_content[message_key] = response_message

    def _ensure_headers(self):
        self['Content-Type'] = self.MEDIA_TYPE
        self['Access-Control-Expose-Headers'] = '*'
        self['Access-Control-Allow-Credentials'] = 'true'

