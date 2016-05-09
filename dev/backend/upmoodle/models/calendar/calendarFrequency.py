from django.db import models


class CalendarFrequency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
