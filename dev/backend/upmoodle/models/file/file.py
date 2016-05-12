import datetime
import hashlib
import time

from django.db import models

from upmoodle.models.base_model import BaseModel
from upmoodle.models.file.fileType import FileType
from upmoodle.models.file.year import Year
from upmoodle.models.level import Level
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.user import User

from upmoodle.models.utils.requestException import RequestExceptionByCode


class File(BaseModel):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Level)
    hash = models.CharField(max_length=512, unique=True)
    name = models.CharField(max_length=256, blank=False)
    filename = models.CharField(max_length=256, blank=False)
    fileType = models.ForeignKey(FileType, default=1)
    year = models.ForeignKey(Year)
    uploaded = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, related_name='file_lastUpdater')
    lastUpdate = models.DateTimeField(auto_now=True)
    lastUpdater = models.ForeignKey(User, related_name='file_updater')
    visible = models.BooleanField(default=True)
    file = models.FileField(upload_to='files')
    text = models.CharField(max_length=2000, blank=True)

    def __init__(self, *args, **kwargs):
        from upmoodle.services.orm.serializers.file import FileSerializer
        super(File, self).__init__(FileSerializer, *args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_binary_sha256(self):
        md5 = hashlib.sha256()
        for chunk in self.file.chunks():
            md5.update(chunk)
        return md5.hexdigest() + str(datetime.datetime.now().microsecond)

    def get_hashed_filename(self):
        return "%s_%s" % (self.hash, str(int(time.time())))

    def save(self, *args, **kwargs):
        self.hash = self.get_binary_sha256()

        self.clean()
        if not self.lastUpdater_id:
            self.lastUpdater = self.uploader
        if self.hash not in self.file.name:  # 1st time uploading
            self.filename = self.file.name
            self.file.name = self.get_hashed_filename()
        super(File, self).save(*args, **kwargs)

    def clean(self):
        self.validate_name()
        self.validate_year()

    def validate_year(self):
        self.year = Year.get_actual_year()

    def validate_name(self):
        if not self.name and self.hash not in self.file.name:
            self.name = self.file.name.split('.')[0]
        elif not self.name:
            raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)

    def update(self, user_update, fields):
        self.year = Year.get_actual_year()
        if fields:
            for field in fields:
                setattr(self, field, getattr(user_update, field))

    @classmethod
    def parse(cls, form, *args, **kwargs):
        fields = kwargs.get('fields', None)
        optional = kwargs.get('optional', False)
        binary = kwargs.get('binary', None)
        if fields:
            filez = File(file=binary)
            return filez.unserialize(fields, form, optional=optional)
        else:
            raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)
