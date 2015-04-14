from django.forms import widgets
from rest_framework import serializers
from rest.models import *


class BannedHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedHash
        field = 'hash'


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class LevelSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    class Meta:
        model = Level
        fields = ('id', 'name', 'type', 'parent')


class UserSerializer(serializers.ModelSerializer):
    rol = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    subjects = LevelSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'rol', 'email', 'nick', 'name', 'profilePic', 'lastTimeActive', 'joined', 'banned', 'subjects')


class UserSimpleSerializer(serializers.ModelSerializer):
    rol = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = ('id', 'rol', 'email', 'nick', 'name', 'profilePic', 'lastTimeActive', 'joined', 'banned')


class NoteBoardSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    author = UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = NoteBoard
        fields = ('id', 'topic', 'text', 'level', 'author', 'created')


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id', 'name')


class CalendarEventSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)
    lastUpdated = UserSerializer(many=False)
    # dates = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dates = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='date'
    )

    class Meta:
        model = Calendar
        fields = ('id', 'title', 'text', 'created', 'lastUpdate', 'author', 'lastUpdated', 'level', 'dates')


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'subject', 'hash', 'name', 'year', 'fileType', 'uploaded', 'uploader', 'lastUpdate', 'lastUpdater', 'visible', 'file')


class ErrorMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ErrorMessage
        fields = ('error',)


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        field = ('message',)