from django.forms import widgets
from rest_framework import serializers
from rest.models import *


class NoteBoardSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = NoteBoard
        fields = ('id', 'topic', 'text', 'level')


class BannedHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedHash
        field = 'hash'


class UserSerializer(serializers.ModelSerializer):
    rol = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = (
            'id', 'rol', 'email', 'nick', 'name', 'profilePic', 'lastTimeActive', 'joined', 'banned', 'sessionToken')


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id', 'name')


class CalendarEventDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEventDate
        fields = ('index', 'hourStart', 'hourEnd', 'allDay', 'frequency')


class CalendarEventSerializer(serializers.ModelSerializer):
    dates = CalendarEventDateSerializer(many=True)

    class Meta:
        model = CalendarRegularEvent
        fields = ('id', 'title', 'text', 'created', 'lastUpdate', 'author', 'lastUpdated', 'level', 'dates')


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'subject', 'hash', 'name', 'year', 'fileType', 'uploaded', 'uploader', 'lastUpdate', 'lastUpdater', 'visible')