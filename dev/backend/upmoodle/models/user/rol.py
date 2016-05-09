from django.db import models


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)  # The more high is the value, the more priority.

    def __unicode__(self):
        return self.name
