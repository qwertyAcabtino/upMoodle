from rest_framework import serializers

from upmoodle.models import BannedHash


class BannedHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedHash
        field = 'hash'
