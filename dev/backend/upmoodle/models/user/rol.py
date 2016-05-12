from django.db import models

from upmoodle.models._base_model import BaseModel


class Rol(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)  # The more high is the value, the more priority.

    def __init__(self, *args, **kwargs):
        from upmoodle.models.serializers import RolSerializer
        super(Rol, self).__init__(RolSerializer, *args, **kwargs)

    def __unicode__(self):
        return self.name
