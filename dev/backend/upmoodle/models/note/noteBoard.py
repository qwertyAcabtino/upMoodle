from django.db import models
from django.utils import timezone

from upmoodle.models._base_model import BaseModel
from upmoodle.models.user import User
from upmoodle.models.utils.validators import validate_length


class NoteBoard(BaseModel):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)
    level = models.ForeignKey('Level')
    author = models.ForeignKey(User, related_name='publisher')
    visible = models.BooleanField(default=True)
    authorized = models.BooleanField(default=True)  # Todo. Remove.
    created = models.DateTimeField(default=timezone.now, editable=True, null=False)

    def __init__(self, *args, **kwargs):
        from upmoodle.models.serializers import NoteBoardSerializer
        super(NoteBoard, self).__init__(NoteBoardSerializer, *args, **kwargs)

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

    def update(self, update_user, fields):
        if fields:
            for field in fields:
                setattr(self, field, getattr(update_user, field))