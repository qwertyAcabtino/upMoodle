from django.db import models
from enum import Enum


class BaseMessage(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)
    msg_key = models.CharField(max_length=20)
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


class OkMessage(BaseMessage):

    @property
    def json(self):
        from rest.orm.serializers import OkMessageSerializer
        data = OkMessageSerializer(self, many=False).data
        dict(data)
        del data['id']
        return data

    class Type(Enum):
        SUCCESS_LOGIN = 1
        EMAIL_CONFIRMED = 2
        RECOVER_PASS_EMAIL = 3
        USER_REMOVED = 4
        USER_UPDATED = 5
        NOTE_UPDATED = 6
        NOTE_REMOVED = 7
        CALENDAR_EVENT_REMOVED = 8
        CALENDAR_UPDATED = 9
        FILE_REMOVED = 10
        ACCOUNT_VALIDATED = 11
        NOTE_CREATED = 12
        FILE_UPLOADED = 13
        FILE_UPDATED = 14
        SUCCESS_LOGOUT = 15
        SUCCESS = 16

        def get(self):
            return OkMessage.objects.get(pk=self.value)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message


class MessageType(Enum):

    SUCCESS_LOGIN = 1
    EMAIL_CONFIRMED = 2
    RECOVER_PASS_EMAIL = 3
    USER_REMOVED = 4
    USER_UPDATED = 5
    NOTE_UPDATED = 6
    NOTE_REMOVED = 7
    CEVENT_REMOVED = 8
    CALENDAR_UPDATED = 9
    FILE_REMOVED = 10
    ACCOUNT_VALIDATED = 11
    NOTE_CREATED = 12
    FILE_UPLOADED = 13
    FILE_UPDATED = 14
    SUCCESS_LOGOUT = 15
    SUCCESS = 16
