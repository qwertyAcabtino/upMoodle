from rest_framework import serializers

from upmoodle.models import Year


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        field = ('id', 'year')
