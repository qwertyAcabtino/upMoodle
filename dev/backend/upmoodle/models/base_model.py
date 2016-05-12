from copy import copy

from django.db import models
from rest_framework.serializers import SerializerMetaclass


class BaseModel(models.Model):

    serializer = SerializerMetaclass

    def __init__(self, serializer, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self.serializer = serializer

    @classmethod
    def query_one(cls, **kwargs):
        user = cls.objects.get(**kwargs)
        return cls.__query(user, many=False)

    @classmethod
    def query_many(cls, **kwargs):
        query_params = kwargs
        users = cls.objects.filter(**query_params)
        return cls.__query(users, many=True)

    @classmethod
    def __query(cls, data=None, many=False):
        return cls().serializer(data, many=many).data

    class Meta:
        abstract = True

    def unserialize(self, fields, form, *args, **kwargs):
        fields_copy = copy(fields)
        optional = kwargs.get('optional', False)

        for field in fields_copy:
            if field in form:
                setattr(self, field, form[field])
            elif optional:
                fields.remove(field)
            else:
                raise KeyError
            # Todo. This is the old code and the new might not be correct. Has to be checked.
            # try:
            #     setattr(self, field, form[field])
            # except KeyError as m:
            #     if not optional:
            #         raise m
            #     else:
            #         fields.remove(field)
        return self
