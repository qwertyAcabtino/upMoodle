from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone

from rest.models.level import Level
from rest.models.message.errorMessage import ErrorMessage
from rest.models.utils.finals import STUDENT
from rest.models.utils.validators import validate_length


class User(models.Model):
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

    class Meta:
        app_label = 'rest'

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
                raise ValidationError(ErrorMessage.Type.EMAIL_INVALID.value)
        except ValidationError as v:
            raise ValidationError(ErrorMessage.Type.EMAIL_INVALID.value)

    def validate_password(self):
        lengthMax = User._meta.get_field('password').max_length
        validate_length(self.password, lengthMax, 8, ErrorMessage.Type.PASSWORD_LENGTH)

    def validate_nick(self):
        lengthMax = User._meta.get_field('nick').max_length
        validate_length(self.nick, lengthMax, 4, ErrorMessage.Type.NICK_LENGTH)

    def validate_name(self):
        lengthMax = User._meta.get_field('name').max_length
        validate_length(self.name, lengthMax, 4, ErrorMessage.Type.NAME_LENGTH)

    def update(self, userUpdate, fields):
        if fields:
            for field in fields:
                setattr(self, field, getattr(userUpdate, field))

    def add_subject(self, subjectPk):
        level = Level.objects.get(id=subjectPk)
        if level.is_subject():
            self.subjects.add(level)
        else:
            raise ValidationError(ErrorMessage.Type.INCORRECT_DATA.value)

    def remove_subject(self, subjectPk):
        level = Level.objects.get(id=subjectPk)
        if level.is_subject():
            self.subjects.remove(level)
        else:
            raise ValidationError(ErrorMessage.Type.INCORRECT_DATA.value)

    def update_subjects(self, subjects):
        self.subjects.clear()
        for subject in subjects:
            self.add_subject(subject)

    @property
    def json(self):
        from rest.services.orm.serializers import UserSerializer
        return UserSerializer(self, many=False).data

    @staticmethod
    def get_signed_user_id(sessionToken):
        return User.objects.get(sessionToken=sessionToken).id

