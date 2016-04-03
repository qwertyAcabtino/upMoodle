import hashlib

from django.core.exceptions import ValidationError
from django.db import models

from rest.MESSAGES_ID import INCORRECT_DATA
from rest.controllers.Exceptions.exceptions import ExtensionError
from rest.models import Year, FileType
from rest.models.level import Level
from rest.models.user import User


class File(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Level)
    hash = models.CharField(max_length=65)
    name = models.CharField(max_length=100, blank=False)
    year = models.ForeignKey(Year)
    fileType = models.ForeignKey(FileType, default=1)
    uploaded = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, related_name='file_lastUpdater')
    lastUpdate = models.DateTimeField(auto_now=True)
    lastUpdater = models.ForeignKey(User, related_name='file_updater')
    visible = models.BooleanField(default=True)
    file = models.FileField(upload_to='files')
    text = models.CharField(max_length=2000, blank=True)

    def __unicode__(self):
        return self.name

    def extension(self):
        index = self.file.name.rfind('.')
        if index == -1 or ((len(self.file.name) - index - 1) > 4):
            raise ExtensionError
        return self.file.name[index + 1:]

    def get_sha256(self):
        md5 = hashlib.sha256()
        for chunk in self.file.chunks():
            md5.update(chunk)
        return md5.hexdigest()

    def get_hashed_filename(self):
        return "%s.%s" % (self.hash, self.file.name.split('.')[-1])

    def save(self, *args, **kwargs):
        self.hash = self.get_sha256()
        self.clean()
        if not self.lastUpdater_id:
            self.lastUpdater = self.uploader
        if self.hash not in self.file.name:
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
            raise ValidationError(INCORRECT_DATA)

    def update(self, userUpdate, fields):
        self.year = Year.get_actual_year()
        if fields:
            for field in fields:
                setattr(self, field, getattr(userUpdate, field))
