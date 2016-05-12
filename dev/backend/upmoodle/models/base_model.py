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
