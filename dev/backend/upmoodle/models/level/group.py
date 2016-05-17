from django.db import models

class ClassGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=100)
    classroom = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

