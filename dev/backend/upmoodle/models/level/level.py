from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.datastructures import MultiValueDictKeyError

from upmoodle.models._base_model import BaseModel
from upmoodle.models.exceptions.messageBasedException import MessageBasedException
from upmoodle.models.message.errorMessage import ErrorMessage


class Level(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.ForeignKey('LevelType')
    visible = models.BooleanField(default=True)
    parent = models.ForeignKey('Level', default=None, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        from upmoodle.models.serializers import LevelSerializer
        super(Level, self).__init__(LevelSerializer, *args, **kwargs)

    def __unicode__(self):
        return self.name

    def is_subject(self):
        return self.type.name == 'subject'

    @classmethod
    def validate_exists(cls, form):
        try:
            fk = form['level_id']
            cls.objects.get(id=fk)
            cls.validate_exists_level(fk)
        except (MultiValueDictKeyError, KeyError):
            raise MessageBasedException(message_id=ErrorMessage.Type.INVALID_LEVEL)

    @staticmethod
    def validate_exists_level(fk):
        try:
            Level.objects.get(id=fk)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    @staticmethod
    def validate_subject_type(level_id):
        assert Level.objects.get(id=level_id).is_subject()
