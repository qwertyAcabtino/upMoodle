from django.views.decorators.csrf import csrf_exempt

from upmoodle.routers.decorators.routing_decorators import authenticated, methods, method
from upmoodle.services.notes import NoteService


@csrf_exempt
@authenticated
@methods(('GET', 'PUT', 'DELETE'))
def note_by_id(request, note_id, session_token=None, data=None, **kwargs):
    service_methods = {
        'GET': NoteService.get_note_by_id,
        'PUT': NoteService.update_note_by_id,
        'DELETE': NoteService.delete_note_by_id,
    }
    return service_methods[request.method](session_token=session_token, note_id=note_id, data=data, **kwargs)


@csrf_exempt
@authenticated
@method('POST')
def note_endpoint(request, session_token=None, data=None, **kwargs):
    return NoteService.add(session_token=session_token, data=data)
