from django.db import models

from upmoodle.models._base_model import BaseModel


class FileType(BaseModel):
    name = models.CharField(max_length=20, blank=False)
    id = models.AutoField(primary_key=True)

    def __init__(self, *args, **kwargs):
        from upmoodle.models.serializers.file import FileTypeSerializer
        super(FileType, self).__init__(FileTypeSerializer, *args, **kwargs)

    def __unicode__(self):
        return self.name
