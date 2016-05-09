from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest.models import Message, OkMessage, ErrorMessage
from rest.orm.serializers import MessageSerializer


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        self['Access-Control-Expose-Headers'] = '*'
        self['Access-Control-Allow-Credentials'] = 'true'


class ResponseJson(HttpResponse):
    def __init__(self, body=None, message_id=None, **kwargs):

        global response_message
        http_code = 200
        response_content = dict()
        if body is not None:
            try:
                response_content['id'] = body.id
            except AttributeError:
                response_content = body

        if message_id:
            if type(message_id.get()) == OkMessage:
                response_message = OkMessage.objects.get(pk=message_id.value).json
            elif type(message_id.get()) == ErrorMessage:
                response_message = ErrorMessage.objects.get(pk=message_id.value)
            http_code = response_message['http_code']
            response_content['message'] = response_message

        content = JSONRenderer().render(response_content)

        kwargs['content_type'] = 'application/json'
        super(ResponseJson, self).__init__(content, status=http_code, **kwargs)
        self['Access-Control-Expose-Headers'] = '*'
        self['Access-Control-Allow-Credentials'] = 'true'


class JSONResponseID(JSONResponse):
    def __init__(self, code):
        message = Message.objects.get(pk=code.value)
        serializer = MessageSerializer(message, many=False)
        super(JSONResponseID, self).__init__(serializer.data, status=200)
