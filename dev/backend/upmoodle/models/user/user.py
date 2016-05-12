from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone

from upmoodle.models.base_model import BaseModel
from upmoodle.models.level import Level
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.utils.finals import STUDENT
from upmoodle.models.utils.validators import validate_length


class User(BaseModel):
    id = models.AutoField(primary_key=True)
    rol = models.ForeignKey('Rol', default=STUDENT)
    email = models.EmailField(max_length=100, unique=True)
    nick = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100)
    profilePic = models.ImageField(upload_to='pics/users', default='static/default_update_avatar_pic.jpeg')
    lastTimeActive = models.DateTimeField(default=timezone.now, null=False, editable=True)
    joined = models.DateTimeField(default=timezone.now, editable=True, null=False)
    banned = models.BooleanField(default=False)
    confirmedEmail = models.BooleanField(default=False)
    sessionToken = models.CharField(max_length=256, blank=True, unique=True)
    subjects = models.ManyToManyField(Level, blank=True)

    def __init__(self, *args, **kwargs):
        from upmoodle.services.orm.serializers import UserSerializer
        super(User, self).__init__(UserSerializer, *args, **kwargs)

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
        from upmoodle.models.utils.requestException import RequestExceptionByCode
        try:
            validate_email(self.email)
            if "@eui.upm.es" not in self.email and "@upm.es" not in self.email and "@alumnos.upm.es" not in self.email:
                raise RequestExceptionByCode(ErrorMessage.Type.EMAIL_INVALID)
        except ValidationError as v:
            raise RequestExceptionByCode(ErrorMessage.Type.EMAIL_INVALID)

    def validate_password(self):
        max_length = User._meta.get_field('password').max_length
        validate_length(self.password, max_length, 8, ErrorMessage.Type.PASSWORD_LENGTH)

    def validate_nick(self):
        max_length = User._meta.get_field('nick').max_length
        validate_length(self.nick, max_length, 4, ErrorMessage.Type.NICK_LENGTH)

    def validate_name(self):
        max_length = User._meta.get_field('name').max_length
        validate_length(self.name, max_length, 4, ErrorMessage.Type.NAME_LENGTH)

    def update(self, updated_user, fields):
        if fields:
            for field in fields:
                setattr(self, field, getattr(updated_user, field))

    def add_subject(self, subject_id):
        level = Level.objects.get(id=subject_id)
        if level.is_subject():
            self.subjects.add(level)
        else:
            from upmoodle.models.utils.requestException import RequestExceptionByCode
            raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)

    def update_subjects(self, subjects):
        self.subjects.clear()
        for subject in subjects:
            self.add_subject(subject)

    @staticmethod
    def get_signed_user_id(session_token):
        return User.objects.get(sessionToken=session_token).id

