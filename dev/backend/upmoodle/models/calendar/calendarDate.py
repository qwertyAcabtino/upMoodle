from django.db import models


class CalendarDate(models.Model):
    id = models.AutoField(primary_key=True)
    calendarId = models.ForeignKey('Calendar', related_name='dates')
    date = models.DateTimeField(null=False)

    def __unicode__(self):
        return self.date.__str__()

