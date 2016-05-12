from copy import copy

from django.db import models
from rest_framework.serializers import SerializerMetaclass

from upmoodle.models import ErrorMessage
from upmoodle.models.utils.requestException import RequestExceptionByCode


class BaseModel(models.Model):

    serializer = SerializerMetaclass

    class Meta:
        abstract = True

    def __init__(self, serializer, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self.serializer = serializer

    # TODO. Remove
    @classmethod
    def query_one(cls, **kwargs):
        user = cls.objects.get(**kwargs)
        return cls.__query(user, many=False)

    # TODO. Remove
    @classmethod
    def query_many(cls, **kwargs):
        query_params = kwargs
        users = cls.objects.filter(**query_params)
        return cls.__query(users, many=True)

    # TODO. Remove
    @classmethod
    def __query(cls, data=None, many=False):
        return cls().serializer(data, many=many).data

    @classmethod
    def get_json(cls, data=None, collection=False):
        return cls().serializer(data, many=collection).data

    @classmethod
    def parse(cls, json, **kwargs):
        obj = cls()
        obj._set_by_json(json, **kwargs)
        return obj

    def _set_by_json(self, json_dict, **kwargs):
        if 'fields' not in kwargs:
            raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)

        optional = kwargs.get('optional', False)
        fields = kwargs.get('fields', None)
        fields_copy = copy(fields)

        for field in fields_copy:
            if field in json_dict:
                setattr(self, field, json_dict[field])
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
