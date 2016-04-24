from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest.models import Message
from rest.orm.serializers import MessageSerializer


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


class JSONResponseID(JSONResponse):

    def __init__(self, code):
        message = Message.objects.get(pk=code.value)
        serializer = MessageSerializer(message, many=False)
        super(JSONResponseID, self).__init__(serializer.data, status=200)

