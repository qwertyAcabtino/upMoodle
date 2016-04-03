from django.db import models


class FileType(models.Model):
    name = models.CharField(max_length=20, blank=False)
    id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return self.name
