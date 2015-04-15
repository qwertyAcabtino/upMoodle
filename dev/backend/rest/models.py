import calendar
import datetime
import os
from django.utils import timezone
from django.core.validators import EmailValidator, validate_email
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

from rest.MESSAGES_ID import NICK_LENGTH, PASSWORD_LENGTH, EMAIL_INVALID, INCORRECT_DATA, NAME_LENGTH
from rest.controllers.Exceptions.exceptions import ExtensionError
from rest.finals import *
import hashlib


# Carrer, course, subject
from rest.validators import validate_length


class ErrorMessage(models.Model):
    id = models.AutoField(primary_key=True)
    error = models.CharField(max_length=200)

    def __unicode__(self):
        return self.error


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message


class LevelType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.ForeignKey('LevelType')
    visible = models.BooleanField(default=True)
    parent = models.ForeignKey('Level', default=None, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def is_subject(self):
        return self.type.name == 'subject'

    @staticmethod
    def validate_exists(form):
        try:
            fk = form['level_id']
            Level.objects.get(id=fk)
            Level.validate_exists_level(fk)
        except MultiValueDictKeyError:
            pass
            # TODO. Solve

    @staticmethod
    def validate_exists_level(fk):
        try:
            Level.objects.get(id=fk)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)  # The more high is the value, the more priority.

    def __unicode__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    rol = models.ForeignKey('Rol', default=STUDENT)
    email = models.EmailField(max_length=100, unique=True)
    nick = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100)
    profilePic = models.ImageField(upload_to='pics/users', default='pics/users/_default.png')
    lastTimeActive = models.DateTimeField(default=timezone.now, null=False, editable=True)
    joined = models.DateTimeField(default=timezone.now, editable=True, null=False)
    banned = models.BooleanField(default=False)
    confirmedEmail = models.BooleanField(default=False)
    sessionToken = models.CharField(max_length=256, blank=True, unique=True)
    subjects = models.ManyToManyField(Level, blank=True)

    def __unicode__(self):
        return self.nick

    def save(self, *args, **kwargs):
        self.clean()  # Custom field validation.
        self.clean_fields()
        self.validate_unique()
        if not self.joined:
            self.joined = timezone.now()
        return super(User, self).save(*args, **kwargs)

    def clean(self):
        self.validate_email()
        self.validate_password()
        self.validate_nick()
        self.validate_name()

    def validate_email(self):
        try:
            validate_email(self.email)
            if not "@eui.upm.es" in self.email and not "@upm.es" in self.email and not "@alumnos.upm.es" in self.email:
                raise ValidationError(EMAIL_INVALID)
        except ValidationError as v:
            raise ValidationError(EMAIL_INVALID)

    def validate_password(self):
        lengthMax = User._meta.get_field('password').max_length
        validate_length(self.password, lengthMax, 8, PASSWORD_LENGTH)

    def validate_nick(self):
        lengthMax = User._meta.get_field('nick').max_length
        validate_length(self.nick, lengthMax, 4, NICK_LENGTH)

    def validate_name(self):
        lengthMax = User._meta.get_field('name').max_length
        validate_length(self.name, lengthMax, 4, NAME_LENGTH)

    def update(self, userUpdate, fields):
        if fields:
            for field in fields:
                setattr(self, field, getattr(userUpdate, field))

    def add_subject(self, subjectPk):
        level = Level.objects.get(id=subjectPk)
        if level.is_subject():
            self.subjects.add(level)
        else:
            raise ValidationError(INCORRECT_DATA)

    def remove_subject(self, subjectPk):
        level = Level.objects.get(id=subjectPk)
        if level.is_subject():
            self.subjects.remove(level)
        else:
            raise ValidationError(INCORRECT_DATA)

    def update_subjects(self, subjects):
        self.subjects.clear()
        for subject in subjects:
            self.add_subject(subject)

    @staticmethod
    def get_signed_user_id(sessionToken):
        return User.objects.get(sessionToken=sessionToken).id


class NoteBoard(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)
    level = models.ForeignKey('Level')
    author = models.ForeignKey(User, related_name='publisher')
    visible = models.BooleanField(default=True)
    authorized = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, editable=True, null=False)

    def __unicode__(self):
        return self.topic

    def save(self, *args, **kwargs):
        self.clean()
        self.clean_fields()
        self.validate_unique()
        super(NoteBoard, self).save(*args, **kwargs)

    def clean(self):
        self.validate_topic()
        self.validate_text()

    def validate_topic(self):
        length = NoteBoard._meta.get_field('topic').max_length
        validate_length(self.topic, length)

    def validate_text(self):
        length = NoteBoard._meta.get_field('text').max_length
        validate_length(self.text, length)

    def update(self, userUpdate, fields):
        if fields:
            for field in fields:
                setattr(self, field, getattr(userUpdate, field))


class CalendarFrequency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


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
            raise ValidationError(INCORRECT_DATA)

    # TODO. Error message.
    def validateDates(self):
        if self.frequency.id != FREQUENCY_UNIQUE and not self.lastDate:
            raise ValidationError(INCORRECT_DATA)
        elif self.lastDate and self.firstDate > self.lastDate:
            raise ValidationError(INCORRECT_DATA)
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
        day = min(sourceDate.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    def update(self, newModel, fields):
        if fields:
            for field in fields:
                setattr(self, field, getattr(newModel, field))


class CalendarDate(models.Model):
    id = models.AutoField(primary_key=True)
    calendarId = models.ForeignKey('Calendar', related_name='dates')
    date = models.DateTimeField(null=False)

    def __unicode__(self):
        return self.date.__str__()


class Year(models.Model):
    id = models.AutoField(primary_key=True)
    verbose = models.CharField(max_length=20)

    def __unicode__(self):
        return self.verbose

    @staticmethod
    def get_actual_year():
        now = datetime.datetime.now()
        if now.month >= 9:
            verbose = "%s/%s" % (now.year, (now.year + 1),)
        else:
            verbose = "%s/%s" % ((now.year - 1), now.year,)
        print verbose
        try:
            return Year.objects.get(verbose=verbose)
        except ObjectDoesNotExist:
            newYear = Year(verbose=verbose)
            newYear.save()
            return newYear


# SHA1. 64 alphabetical chars
class BannedHash(models.Model):
    hash = models.CharField(primary_key=True, max_length=65)

    def __unicode__(self):
        return self.hash


class File(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Level)
    hash = models.CharField(max_length=65)
    name = models.CharField(max_length=100, blank=False)
    year = models.ForeignKey(Year)
    fileType = models.CharField(max_length=50, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, related_name='file_lastUpdater')
    lastUpdate = models.DateTimeField(auto_now=True)
    lastUpdater = models.ForeignKey(User, related_name='file_updater')
    visible = models.BooleanField(default=True)
    file = models.FileField(upload_to='files')
    text = models.CharField(max_length=2000, blank=True)

    def __unicode__(self):
        return self.name

    def extension(self):
        index = self.file.name.rfind('.')
        if index == -1 or ((len(self.file.name) - index - 1) > 4):
            raise ExtensionError
        return self.file.name[index + 1:]

    def get_sha256(self):
        md5 = hashlib.sha256()
        for chunk in self.file.chunks():
            md5.update(chunk)
        return md5.hexdigest()

    def get_hashed_filename(self):
        return "%s.%s" % (self.hash, self.file.name.split('.')[-1])

    def save(self, *args, **kwargs):
        self.hash = self.get_sha256()
        self.clean()
        if not self.lastUpdater_id:
            self.lastUpdater = self.uploader
        if self.hash not in self.file.name:
            self.file.name = self.get_hashed_filename()
        super(File, self).save(*args, **kwargs)

    def clean(self):
        self.validate_name()
        self.validate_year()

    def validate_year(self):
        self.year = Year.get_actual_year()

    def validate_name(self):
        if not self.name and self.hash not in self.file.name:
            self.name = self.file.name.split('.')[0]
        elif not self.name:
            raise ValidationError(INCORRECT_DATA)

    def update(self, userUpdate, fields):
        self.year = Year.get_actual_year()
        if fields:
            for field in fields:
                setattr(self, field, getattr(userUpdate, field))


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class FileTag(models.Model):
    idFile = models.ForeignKey(File)
    idTag = models.ForeignKey(Tag)

    def __unicode__(self):
        return '%s - %s' % (self.idFile, self.idTag)


class FileReportList(models.Model):
    idFile = models.ForeignKey(File)
    idReporter = models.ForeignKey(User)
    comment = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s @ %s' % (self.comment[0:10], self.idFile)


class FileComments(models.Model):
    id = models.AutoField(primary_key=True)
    idFile = models.ForeignKey(File)
    idAuthor = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)

    def __unicode__(self):
        return '%s @ %s' % (self.text[0:10], self.idFile)