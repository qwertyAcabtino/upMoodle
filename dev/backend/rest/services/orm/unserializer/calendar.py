from rest.models import Calendar
from rest.models.message.errorMessage import ErrorMessage
from rest.models.utils.requestException import RequestExceptionByCode
from rest.services.orm.unserializer import unserialize


def unserialize_calendar(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    optional = kwargs.get('optional', False)
    if fields:
        calendar = Calendar()
        return unserialize(calendar, fields, form, optional=optional)
    else:
        raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)
