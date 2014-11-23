from copy import copy
from django.http.request import QueryDict
from django.utils.datastructures import MultiValueDictKeyError
from rest.MESSAGES_ID import INCORRECT_DATA
from rest.controllers.Exceptions.requestException import RequestExceptionByCode
from rest.models import User


def get_value(form, key):
    try:
        return form[key]
    except KeyError as k:
        return ''


def unserialize_user(form, cookie):
    user = User()
    user.email = get_value(form, 'email')
    user.password = get_value(form, 'password')
    user.nick = get_value(form, 'nick')
    user.sessionToken = cookie
    return user


def unserialize_user_2(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    fieldsCopy = copy(fields)
    sessionToken = kwargs.get('sessionToken', None)
    optional = kwargs.get('optional', False)
    if fields:
        user = User()
        for field in fieldsCopy:
            #If the field doesnt exists raises an MultiValueDictKeyError
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