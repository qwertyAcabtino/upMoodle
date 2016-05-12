from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.datastructures import MultiValueDictKeyError

from upmoodle.models.message.errorMessage import ErrorMessage

from upmoodle.models.utils.requestException import RequestExceptionByCode


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

    @classmethod
    def validate_exists(cls, form):
        try:
            fk = form['level_id']
            cls.objects.get(id=fk)
            cls.validate_exists_level(fk)
        except (MultiValueDictKeyError, KeyError):
            raise RequestExceptionByCode(ErrorMessage.Type.INVALID_LEVEL)

    @staticmethod
    def validate_exists_level(fk):
        try:
            Level.objects.get(id=fk)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    @staticmethod
    def validate_subject_type(level_id):
        assert Level.objects.get(id=level_id).is_subject()
