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


class CalendarEventSerializer(serializers.ModelSerializer):
    dates = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = CalendarRegularEvent
        fields = ('id', 'title', 'text', 'created', 'lastUpdate', 'author', 'lastUpdated', 'level', 'dates', 'regular')