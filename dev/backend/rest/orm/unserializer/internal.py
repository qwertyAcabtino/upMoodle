# noinspection PyUnresolvedReferences
from copy import copy

from django.utils.datastructures import MultiValueDictKeyError

from rest.exceptions.requestException import RequestExceptionByCode


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
