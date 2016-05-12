from rest_framework import serializers

from upmoodle.models import FileType, File
from upmoodle.models.serializers import YearSerializer, UserSimpleSerializer


class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileType
        fields = ('id', 'name',)


class FileSerializer(serializers.ModelSerializer):
    year = YearSerializer(many=False)
    uploader = UserSimpleSerializer(many=False)
    lastUpdater = UserSimpleSerializer(many=False)
    fileType = FileTypeSerializer(many=False)

    class Meta:
        model = File
        fields = (
            'id', 'subject', 'hash', 'name', 'year', 'fileType', 'uploaded', 'uploader', 'lastUpdate', 'lastUpdater',
            'visible', 'filename', 'text')
