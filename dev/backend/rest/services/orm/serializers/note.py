from rest_framework import serializers

from rest.models import NoteBoard
from rest.services.orm.serializers import LevelSerializer
from rest.services.orm.serializers import UserSimpleSerializer


class NoteBoardSerializer(serializers.ModelSerializer):
    level = LevelSerializer(many=False, read_only=True)
    author = UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = NoteBoard
        fields = ('id', 'topic', 'text', 'level', 'author', 'created')
