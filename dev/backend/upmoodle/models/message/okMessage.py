from enum import Enum

from upmoodle.models.message.baseMessage import BaseMessage


class OkMessage(BaseMessage):

    @property
    def json(self):
        from upmoodle.models.serializers import OkMessageSerializer
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
        SUCCESS_SIGNUP = 17

        def get(self):
            return OkMessage.objects.get(pk=self.value)
