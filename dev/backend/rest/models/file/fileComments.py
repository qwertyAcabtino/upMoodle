from django.db import models

from rest.models import File
from rest.models.user import User


class FileComments(models.Model):
    id = models.AutoField(primary_key=True)
    idFile = models.ForeignKey(File)
    idAuthor = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)

    def __unicode__(self):
        return '%s @ %s' % (self.text[0:10], self.idFile)