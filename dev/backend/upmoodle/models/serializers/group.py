from rest_framework import serializers

from upmoodle.models import ClassGroup


class ClassGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = ('id', 'name', 'classroom')

