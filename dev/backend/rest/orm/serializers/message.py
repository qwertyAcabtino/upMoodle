from rest_framework import serializers

from rest.models import ErrorMessage, OkMessage


class ErrorMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorMessage
        fields = ('text', 'http_code', 'msg_key',)


class OkMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OkMessage
        field = ('text', 'http_code', 'msg_key', )
