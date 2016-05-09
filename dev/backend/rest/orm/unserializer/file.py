from rest.models import File, ErrorMessage
from rest.models.message.errorMessage import ErrorMessage
from rest.orm.unserializer.internal import *


def unserialize_file(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    optional = kwargs.get('optional', False)
    if fields:
        filez = File()
        return unserialize(filez, fields, form, optional=optional)
    else:
        raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)


def unserialize_file_binary(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    optional = kwargs.get('optional', False)
    binary = kwargs.get('binary', None)
    if fields:
        filez = File(file=binary)
        return unserialize(filez, fields, form, optional=optional)
    else:
        raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)
