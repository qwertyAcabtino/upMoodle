from rest_framework import serializers

from rest.models import Level


class LevelSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = Level
        fields = ('id', 'name', 'type', 'parent')
