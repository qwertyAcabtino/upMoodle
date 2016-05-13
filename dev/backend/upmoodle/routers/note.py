from django.views.decorators.csrf import csrf_exempt

from upmoodle.controllers.decorators.exceptions import zero_exceptions
from upmoodle.controllers.decorators.router import authenticated, methods, method
from upmoodle.models import OkMessage
from upmoodle.routers.response.jsonfactory import JsonResponseFactory
from upmoodle.services.notes import NoteService


@csrf_exempt
@authenticated
@methods(('GET', 'PUT', 'DELETE'))
@zero_exceptions
def note_by_id(request, note_id, session_token=None, data=None, **kwargs):

    def delete(session_token=session_token, note_id=note_id, data=data, **kwargs):
        NoteService.delete_note_by_id(session_token=session_token, note_id=note_id, data=data, **kwargs)
        return JsonResponseFactory().ok(message_id=OkMessage.Type.NOTE_REMOVED).build()

    def update(session_token=session_token, note_id=note_id, data=data, **kwargs):
        NoteService.update_note_by_id(session_token=session_token, note_id=note_id, data=data, **kwargs)
        return JsonResponseFactory().ok(message_id=OkMessage.Type.NOTE_UPDATED).build()

    def get(session_token=session_token, note_id=note_id, data=data, **kwargs):
        note_in = NoteService.get_note_by_id(session_token=session_token, note_id=note_id, data=data, **kwargs)
        return JsonResponseFactory().ok().body(obj=note_in).build()

    service_methods = {
        'GET': get,
        'PUT': update,
        'DELETE': delete,
    }
    return service_methods[request.method](session_token=session_token, note_id=note_id, data=data, **kwargs)


@csrf_exempt
@authenticated
@method('POST')
@zero_exceptions
def note_endpoint(request, session_token=None, data=None, **kwargs):
    new_note = NoteService.add(session_token=session_token, data=data)
    return JsonResponseFactory().ok(message_id=OkMessage.Type.NOTE_CREATED).identity(obj=new_note).build()

