from rest_framework import serializers

from upmoodle.models import NoteBoard
from upmoodle.services.orm.serializers import LevelSerializer
from upmoodle.services.orm.serializers import UserSimpleSerializer


class NoteBoardSerializer(serializers.ModelSerializer):
    level = LevelSerializer(many=False, read_only=True)
    author = UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = NoteBoard
        fields = ('id', 'topic', 'text', 'level', 'author', 'created')
