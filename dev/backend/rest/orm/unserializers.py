from copy import copy
from django.http.request import QueryDict
from django.utils.datastructures import MultiValueDictKeyError
from rest.MESSAGES_ID import INCORRECT_DATA
from rest.controllers.Exceptions.requestException import RequestExceptionByCode
from rest.models import User, NoteBoard, Calendar


def get_value(form, key):
    try:
        return form[key]
    except KeyError as k:
        return ''


def unserialize_user(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    fieldsCopy = copy(fields)
    sessionToken = kwargs.get('sessionToken', None)
    optional = kwargs.get('optional', False)
    if fields:
        user = User()
        for field in fieldsCopy:
            # If the field doesnt exists raises an MultiValueDictKeyError
            try:
                setattr(user, field, form[field])
            except MultiValueDictKeyError as m:
                if not optional:
                    raise m
                else:
                    fields.remove(field)
        if sessionToken:
            user.sessionToken = sessionToken
        return user
    else:
        raise RequestExceptionByCode(INCORRECT_DATA)


def unserialize_note(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    optional = kwargs.get('optional', False)
    if fields:
        note = NoteBoard()
        return unserialize(note, fields, form, optional=optional)
    else:
        raise RequestExceptionByCode(INCORRECT_DATA)


def unserialize_calendar(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    optional = kwargs.get('optional', False)
    if fields:
        calendar = Calendar()
        return unserialize(calendar, fields, form, optional=optional)
    else:
        raise RequestExceptionByCode(INCORRECT_DATA)


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