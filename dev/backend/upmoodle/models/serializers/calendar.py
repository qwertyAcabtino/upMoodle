from rest_framework import serializers

from upmoodle.models import Calendar
from upmoodle.models.serializers import UserSerializer


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
        fields = ('id', 'title', 'text', 'created', 'lastUpdate', 'author', 'lastUpdated', 'level', 'dates', 'allDay', 'hourStart', 'hourEnd')
