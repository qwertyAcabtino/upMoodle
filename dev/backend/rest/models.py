import datetime
from django.utils import timezone
from django.core.validators import EmailValidator, validate_email
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

from rest.MESSAGES_ID import NICK_LENGTH, PASSWORD_LENGTH, EMAIL_INVALID
from rest.controllers.Exceptions.exceptions import ExtensionError
from rest.finals import *



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
    profilePic = models.ImageField(upload_to='pics/users', default='_default.png')
    lastTimeActive = models.DateTimeField(default=timezone.now, null=False, editable=True)
    joined = models.DateTimeField(default=timezone.now, editable=True, null=False)
    banned = models.BooleanField(default=False)
    confirmedEmail = models.BooleanField(default=False)
    sessionToken = models.CharField(max_length=256, blank=True, unique=True)

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

    def validate_email(self):
        try:
            validate_email(self.email)
            if not "@eui.upm.es" in self.email and not "@upm.es" in self.email:
                raise ValidationError(EMAIL_INVALID)
        except ValidationError as v:
            raise ValidationError(EMAIL_INVALID)

    def validate_password(self):
        lengthMax = User._meta.get_field('password').max_length
        validate_length(self.password, lengthMax, 8, PASSWORD_LENGTH)

    def validate_nick(self):
        lengthMax = User._meta.get_field('nick').max_length
        validate_length(self.nick, lengthMax, 4, NICK_LENGTH)

    def update(self, userUpdate, fields):
        if fields:
            for field in fields:
                setattr(self, field, getattr(userUpdate, field))

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


# SHA1. 64 alphabetical chars
class BannedHash(models.Model):
    hash = models.CharField(primary_key=True, max_length=65)

    def __unicode__(self):
        return self.hash


class CalendarFrequency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class CalendarRegularEvent(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=2000)
    created = models.DateField(auto_now_add=True)
    lastUpdate = models.DateField(auto_now=True)
    author = models.ForeignKey(User, null=False, related_name='regular_lastUpdated')
    lastUpdated = models.ForeignKey(User, null=False, related_name='regular_author')
    level = models.ForeignKey('Level')

    def __unicode__(self):
        return self.title


class CalendarEventDate(models.Model):
    id = models.AutoField(primary_key=True)
    idEvent = models.ForeignKey(CalendarRegularEvent, related_name='dates')
    index = models.IntegerField(default=1)
    hourStart = models.TimeField(null=True)
    hourEnd = models.TimeField(null=True)
    firstDate = models.DateField(auto_created=False)
    allDay = models.BooleanField(default=False)
    frequency = models.ForeignKey('CalendarFrequency', default=DEFAULT_FREQUENCY)

    def __unicode__(self):
        return '[%s to %s] %s' % (self.hourStart, self.hourEnd, self.frequency)


class Year(models.Model):
    id = models.AutoField(primary_key=True)
    verbose = models.CharField(max_length=20)

    def __unicode__(self):
        return self.verbose


class File(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Level)
    hash = models.CharField(max_length=65)
    name = models.CharField(max_length=100)
    year = models.ForeignKey(Year)
    fileType = models.CharField(max_length=50)
    uploaded = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, related_name='file_lastUpdater')
    lastUpdate = models.DateTimeField(auto_now=True)
    lastUpdater = models.ForeignKey(User, related_name='file_updater')
    visible = models.BooleanField(default=True)
    file = models.FileField(upload_to='files')

    def __unicode__(self):
        return self.name

    def extension(self):
        index = self.file.name.rfind('.')
        if index == -1 or ((len(self.file.name) - index - 1) > 4):
            raise ExtensionError
        return self.file.name[index + 1:]


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
