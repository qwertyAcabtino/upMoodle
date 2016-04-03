from rest.models import Calendar
from rest.orm.unserializer.internal import *


def unserialize_calendar(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    optional = kwargs.get('optional', False)
    if fields:
        calendar = Calendar()
        return unserialize(calendar, fields, form, optional=optional)
    else:
        raise RequestExceptionByCode(INCORRECT_DATA)
