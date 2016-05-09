from upmoodle.models import NoteBoard
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.utils.requestException import RequestExceptionByCode
from upmoodle.services.orm.unserializer import unserialize


def unserialize_note(form, *args, **kwargs):
    fields = kwargs.get('fields', None)
    optional = kwargs.get('optional', False)
    if fields:
        note = NoteBoard()
        return unserialize(note, fields, form, optional=optional)
    else:
        raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)
