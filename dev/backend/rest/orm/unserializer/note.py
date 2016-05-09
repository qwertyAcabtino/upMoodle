from rest.models import NoteBoard
from rest.models.message.errorMessage import ErrorMessage
from rest.orm.unserializer.internal import *


def unserialize_note(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    optional = kwargs.get('optional', False)
    if fields:
        note = NoteBoard()
        return unserialize(note, fields, form, optional=optional)
    else:
        raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)
