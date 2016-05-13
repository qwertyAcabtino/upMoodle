from django.views.decorators.csrf import csrf_exempt

from upmoodle.controllers.decorators.exceptions import zero_exceptions
from upmoodle.controllers.decorators.router import authenticated, methods, method
from upmoodle.models import OkMessage
from upmoodle.routers.response.factory import ResponseFactory
from upmoodle.services.notes import NoteService


@zero_exceptions
@csrf_exempt
@authenticated
@methods(('GET', 'PUT', 'DELETE'))
def note_by_id(request, note_id, session_token=None, data=None, **kwargs):

    def delete(session_token=session_token, note_id=note_id, data=data, **kwargs):
        NoteService.delete_note_by_id(session_token=session_token, note_id=note_id, data=data, **kwargs)
        return ResponseFactory().ok(message_id=OkMessage.Type.NOTE_REMOVED).build()

    def update(session_token=session_token, note_id=note_id, data=data, **kwargs):
        NoteService.update_note_by_id(session_token=session_token, note_id=note_id, data=data, **kwargs)
        return ResponseFactory().ok(message_id=OkMessage.Type.NOTE_UPDATED).build()

    def get(session_token=session_token, note_id=note_id, data=data, **kwargs):
        note_in = NoteService.get_note_by_id(session_token=session_token, note_id=note_id, data=data, **kwargs)
        return ResponseFactory().ok().body(obj=note_in).build()

    service_methods = {
        'GET': get,
        'PUT': update,
        'DELETE': delete,
    }
    return service_methods[request.method](session_token=session_token, note_id=note_id, data=data, **kwargs)


@zero_exceptions
@csrf_exempt
@authenticated
@method('POST')
def note_endpoint(request, session_token=None, data=None, **kwargs):
    new_note = NoteService.add(session_token=session_token, data=data)
    return ResponseFactory().ok(message_id=OkMessage.Type.NOTE_CREATED).identity(obj=new_note).build()

