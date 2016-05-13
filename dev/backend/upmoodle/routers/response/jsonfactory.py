from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from upmoodle.models import OkMessage, ErrorMessage


class JsonResponseFactory:

    def __init__(self):
        self.response = dict()
        self.obj = None
        self._identity = False
        self._media_type = 'application/json'
        self.http_code = 200

    def ok(self, message_id=OkMessage.Type.SUCCESS):
        message = message_id.get()
        self.response.__setitem__('message', message.json)
        self.http_code = message.http_code
        return self

    def error(self, message_id=ErrorMessage.Type.INCORRECT_DATA, **kwargs):
        message = message_id.get()
        self.response.__setitem__('error', message.json)
        self.http_code = message.http_code
        exception = kwargs.get('exception', None)
        if exception:
            if hasattr(exception, 'stack_trace'):
                stack_trace = exception.stack_trace
            else:
                stack_trace = self.__get_stack_trace(kwargs.get('exception'))
            self.response.get('error', dict())['text'] = stack_trace
        return self

    def __get_stack_trace(self, exception):
        if len(exception.message):
            return exception.message
        elif hasattr(exception, 'messages') and len(exception.messages):
            return '\n. '.join(exception.messages)

    def body(self, obj=None):
        self.obj = obj
        return self

    def identity(self, obj=None):
        self.obj = obj.id
        self._identity = True
        return self

    def media_type(self, media_type='application/json'):
        self._media_type = media_type
        return self

    def build(self):
        switcher = {
            'application/json': self.get_json_response,
            'application/octet-stream': self.get_octet_stream_response
        }
        return switcher.get(self._media_type)()

    def get_json_response(self):
        if self.obj and not self._identity:
            global object_json
            try:
                object_json = type(self.obj).get_json(self.obj, collection=False)
            except Exception:
                object_json = self.obj.model.get_json(self.obj, collection=True)
            self.response.__setitem__('data', object_json)
        elif self.obj and self._identity:
            self.response.__setitem__('data', dict())
            self.response.get('data').__setitem__('id', self.obj)

        response_json = JSONRenderer().render(self.response)
        http_response = self._ensure_headers(HttpResponse(response_json, content_type=self._media_type, status=self.http_code))
        return http_response

    def get_octet_stream_response(self):
        http_response = HttpResponse(self.obj.file)
        http_response['Content-Disposition'] = 'attachment; filename=' + self.obj.filename
        return http_response

    def _ensure_headers(self, http_response):
        http_response['Content-Type'] = self._media_type
        http_response['Access-Control-Expose-Headers'] = '*'
        http_response['Access-Control-Allow-Credentials'] = 'true'
        return http_response
