from copy import copy

from django.db import models
from rest_framework.serializers import SerializerMetaclass

from upmoodle.models import ErrorMessage
from upmoodle.models.exceptions.messageBasedException import MessageBasedException


class BaseModel(models.Model):

    serializer = SerializerMetaclass

    class Meta:
        abstract = True

    def __init__(self, serializer, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self.serializer = serializer

    @classmethod
    def get_flatten_object(cls, data=None, collection=False):
        return cls().serializer(data, many=collection).data

    @classmethod
    def parse(cls, json, **kwargs):
        obj = cls()
        obj._set_by_json(json, **kwargs)
        return obj

    def _set_by_json(self, json_dict, **kwargs):
        if 'fields' not in kwargs:
            raise MessageBasedException(message_id=ErrorMessage.Type.INCORRECT_DATA)

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
