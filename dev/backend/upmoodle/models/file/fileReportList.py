from django.db import models

from upmoodle.models import File
from upmoodle.models.user import User


class FileReportList(models.Model):
    idFile = models.ForeignKey(File)
    idReporter = models.ForeignKey(User)
    comment = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s @ %s' % (self.comment[0:10], self.idFile)

