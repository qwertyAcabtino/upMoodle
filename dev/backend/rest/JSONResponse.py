from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest.models import Message, ErrorMessage, OkMessage
from rest.orm.serializers import MessageSerializer
from rest.orm.serializers.message import OkMessageSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        self['Access-Control-Expose-Headers'] = '*'
        self['Access-Control-Allow-Credentials'] = 'true'


class JsonOkResponse(HttpResponse):
    def __init__(self, body=None, message_id=None, **kwargs):

        message = OkMessage.objects.get(pk=message_id.value)
        message_serialized = OkMessageSerializer(message, many=False)
        content = JSONRenderer().render({
            "id": body.id,
            "message": message_serialized
        })
        content.id = body.id
        content.__setattr__('message', message_serialized.data)

        kwargs['content_type'] = 'application/json'
        super(JsonOkResponse, self).__init__(content, status=message.http_code ** kwargs)
        self['Access-Control-Expose-Headers'] = '*'
        self['Access-Control-Allow-Credentials'] = 'true'


class JSONResponseID(JSONResponse):
    def __init__(self, code):
        message = Message.objects.get(pk=code.value)
        serializer = MessageSerializer(message, many=False)
        super(JSONResponseID, self).__init__(serializer.data, status=200)


class JSONResponseID(JSONResponse):
    def __init__(self, code):
        message = Message.objects.get(pk=code.value)
        serializer = MessageSerializer(message, many=False)
        super(JSONResponseID, self).__init__(serializer.data, status=200)
