from django.db import models
from enum import Enum


class BaseMessage(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)
    http_code = models.IntegerField(default=None)

    class Meta:
        abstract = True

    class Type(Enum):

        class Meta:
            abstract = True

        def get(self):
            pass

    def __unicode__(self):
        return self.text
