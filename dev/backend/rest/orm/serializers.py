from django.forms import widgets
from rest_framework import serializers
from rest.models import *


class NoteBoardSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = NoteBoard
        fields = ('id', 'topic', 'text', 'level', 'author')


class BannedHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedHash
        field = 'hash'


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    rol = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = ('id', 'rol', 'email', 'nick', 'name', 'profilePic', 'lastTimeActive', 'joined', 'banned')


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id', 'name')


class CalendarEventSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)

    class Meta:
        model = CalendarRegularEvent
        fields = ('id', 'title', 'text', 'created', 'lastUpdate', 'author', 'lastUpdated', 'level')


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'subject', 'hash', 'name', 'year', 'fileType', 'uploaded', 'uploader', 'lastUpdate', 'lastUpdater', 'visible')


class ErrorMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ErrorMessage
        fields = ('error',)


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        field = ('message',)