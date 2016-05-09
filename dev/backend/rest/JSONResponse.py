from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest.models import OkMessage, ErrorMessage


class ResponseJson(HttpResponse):

    response_content = dict()
    http_code = 200
    media_type = 'application/json'

    def __init__(self, body=None, message_id=None, **kwargs):

        self._set_response_body(body)
        self._set_response_message(message_id, **kwargs)
        content = JSONRenderer().render(self.response_content)
        super(ResponseJson, self).__init__(content, status=self.http_code)
        self._ensure_headers()

    def _set_response_message(self, message_id, **kwargs):
        global response_message
        if message_id:
            if type(message_id.get()) == OkMessage:
                response_message = OkMessage.objects.get(pk=message_id.value).json
            elif type(message_id.get()) == ErrorMessage:
                response_message = ErrorMessage.objects.get(pk=message_id.value).json

            self.http_code = response_message['http_code']
            self.response_content['message'] = response_message
            if 'stack_trace' in kwargs:
                self.response_content['message']['text'] += ". " + kwargs['stack_trace']

    def _set_response_body(self, body):
        if body is not None:
            try:
                self.response_content['id'] = body.id
            except AttributeError:
                self.response_content = body

    def _ensure_headers(self):
        self['Content-Type'] = self.media_type
        self['Access-Control-Expose-Headers'] = '*'
        self['Access-Control-Allow-Credentials'] = 'true'
