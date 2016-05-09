from copy import copy

from upmoodle.models import User
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.utils.requestException import RequestExceptionByCode


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
            except KeyError as m:
                if not optional:
                    raise m
                else:
                    fields.remove(field)
        if sessionToken:
            user.sessionToken = sessionToken
        return user
    else:
        raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)
