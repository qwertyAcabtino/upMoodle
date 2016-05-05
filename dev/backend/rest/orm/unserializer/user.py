from rest.models import User
from rest.models.message.errorMessage import ErrorMessageType
from rest.orm.unserializer.internal import *


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
        raise RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA)
