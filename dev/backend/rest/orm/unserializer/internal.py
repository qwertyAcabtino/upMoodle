# noinspection PyUnresolvedReferences
from rest.controllers.Exceptions.requestException import RequestExceptionByCode
from django.utils.datastructures import MultiValueDictKeyError
from copy import copy


def unserialize(model, fields, form, *args, **kwargs):
    fieldsCopy = copy(fields)
    optional = kwargs.get('optional', False)

    for field in fieldsCopy:
        # If the field doesnt exists raises an MultiValueDictKeyError
        try:
            setattr(model, field, form[field])
        except MultiValueDictKeyError as m:
            if not optional:
                raise m
            else:
                fields.remove(field)
    return model
