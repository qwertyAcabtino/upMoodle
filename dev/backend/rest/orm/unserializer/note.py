from rest.models import NoteBoard
from rest.orm.unserializer.common import *


def unserialize_note(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    optional = kwargs.get('optional', False)
    if fields:
        note = NoteBoard()
        return unserialize(note, fields, form, optional=optional)
    else:
        raise RequestExceptionByCode(INCORRECT_DATA)
