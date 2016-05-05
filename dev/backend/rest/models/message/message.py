from django.db import models
from enum import Enum


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
