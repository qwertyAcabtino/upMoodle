from rest_framework import serializers

from rest.models import BannedHash


class BannedHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedHash
        field = 'hash'
