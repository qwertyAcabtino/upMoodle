import datetime

from django.core.exceptions import ValidationError
from django.db import models

import rest.models.calendar
from rest.models.calendar.calendarDate import CalendarDate
from rest.models.message.errorMessage import ErrorMessage
from rest.models.user import User
from rest.models.utils.finals import *


class Calendar(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=2000)
    created = models.DateField(auto_now_add=True)
    lastUpdate = models.DateField(auto_now=True)
    author = models.ForeignKey(User, null=False, related_name='regular_lastUpdated')
    lastUpdated = models.ForeignKey(User, null=False, related_name='regular_author')
    level = models.ForeignKey('Level')
    hourStart = models.TimeField(blank=True)
    hourEnd = models.TimeField(blank=True)
    firstDate = models.DateField(auto_created=False)
    lastDate = models.DateField(auto_created=False, blank=True, null=True)
    allDay = models.BooleanField(default=False)
    frequency = models.ForeignKey('CalendarFrequency', default=DEFAULT_FREQUENCY)

    def __unicode__(self):
        return self.title

    def delete(self, *args, **kwargs):
        CalendarDate.objects.filter(id=self.id).delete()
        return super(Calendar, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.clean()  # Custom field validation.
        self.clean_fields()
        self.validate_unique()
        returnValue = super(Calendar, self).save(*args, **kwargs)
        CalendarDate.objects.filter(calendarId=self).delete()
        if self.frequency.id != FREQUENCY_UNIQUE:
            self.setCalendarDates()
        else:
            self.setCalendarDate(self.firstDate)
        return returnValue

    def clean(self):
        self.validateHours()
        self.validateDates()

    # TODO. Error message.
    # TODO. hourStart > hourEnd.
    def validateHours(self):
        if not self.allDay and (not self.hourStart or not self.hourEnd):
            raise ValidationError(ErrorMessage.Type.INCORRECT_DATA.value)

    # TODO. Error message.
    def validateDates(self):
        if self.frequency.id != FREQUENCY_UNIQUE and not self.lastDate:
            raise ValidationError(ErrorMessage.Type.INCORRECT_DATA.value)
        elif self.lastDate and self.firstDate > self.lastDate:
            raise ValidationError(ErrorMessage.Type.INCORRECT_DATA.value)
        elif not self.lastDate:
            self.lastDate = self.firstDate

    def setCalendarDates(self):
        initValue = self.firstDate
        while True:
            if initValue <= self.lastDate:
                self.setCalendarDate(initValue)
                initValue = self.getNextValue(initValue)
            else:
                break

    def setCalendarDate(self, date):
        calendarDate = CalendarDate(calendarId=self)
        calendarDate.date = date
        calendarDate.save()

    """
    http://stackoverflow.com/questions/4130922/how-to-increment-datetime-month-in-python
    http://stackoverflow.com/questions/100210/what-is-the-standard-way-to-add-n-seconds-to-datetime-time-in-python
    http://www.dotnetperls.com/datetime-python
    """

    def getNextValue(self, date):
        if self.frequency.id == FREQUENCY_DAY:
            return date + datetime.timedelta(1)
        elif self.frequency.id == FREQUENCY_WEEK:
            return date + datetime.timedelta(7)
        elif self.frequency.id == FREQUENCY_MONTH:
            return self.iterateMonths(date, 1)
        return None

    @staticmethod
    def iterateMonths(sourceDate, months):
        month = sourceDate.month - 1 + months
        year = sourceDate.year + month / 12
        month = month % 12 + 1
        day = min(sourceDate.day, rest.models.calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    def update(self, newModel, fields):
        if fields:
            for field in fields:
                setattr(self, field, getattr(newModel, field))

