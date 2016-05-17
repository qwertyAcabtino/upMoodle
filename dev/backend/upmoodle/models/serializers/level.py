from rest_framework import serializers

from upmoodle.models import Level
from upmoodle.models.serializers.group import ClassGroupSerializer


class LevelSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    classGroup = ClassGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Level
        fields = ('id', 'name', 'type', 'parent', 'classGroup')
