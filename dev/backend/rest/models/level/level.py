from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.datastructures import MultiValueDictKeyError

from rest.models.message.errorMessage import ErrorMessageType


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
        except (MultiValueDictKeyError, KeyError):
            raise ValidationError(ErrorMessageType.INVALID_LEVEL.value)

    @staticmethod
    def validate_exists_level(fk):
        try:
            Level.objects.get(id=fk)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    @staticmethod
    def validate_subject_type(level_id):
        assert Level.objects.get(id=level_id).is_subject()
