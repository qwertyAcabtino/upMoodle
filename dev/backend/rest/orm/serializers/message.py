from rest_framework import serializers

from rest.models import Message, ErrorMessage, OkMessage


class ErrorMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorMessage
        fields = ('error',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        field = ('message',)


class OkMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OkMessage
        field = ('message', 'message_code', )
