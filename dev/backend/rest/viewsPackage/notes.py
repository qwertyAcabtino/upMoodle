from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.MESSAGES_ID import INCORRECT_DATA, NOTE_UPDATED
from rest.controllers.Exceptions.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from rest.controllers.controllers import check_signed_in_request, check_authorized_author
from rest.models import NoteBoard, Level
from rest.orm.serializers import NoteBoardSerializer
from rest.orm.unserializers import unserialize_note


@csrf_exempt
def note_get(request, pk):
    try:
        check_signed_in_request(request, 'GET')
        note = NoteBoard.objects.get(id=pk)
        serializer = NoteBoardSerializer(note, many=False)
        return JSONResponse(serializer.data)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except OverflowError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


@csrf_exempt
def note_put(request, pk):
    try:
        noteOriginal = NoteBoard.objects.get(id=pk)

        check_signed_in_request(request, 'POST')
        check_authorized_author(request, noteOriginal.author_id)

        form = request.POST
        Level.validate_exists(form)
        fields = ['topic', 'text', 'level_id']
        noteUpdated = unserialize_note(form, fields=fields, optional=True)
        noteOriginal.update(noteUpdated, fields)
        noteOriginal.save()
        return JSONResponseID(NOTE_UPDATED)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except ValidationError as v:
        return RequestExceptionByMessage(v).jsonResponse


@csrf_exempt
# TODO.
def note_delete(request, pk):
    try:
        check_signed_in_request(request, method='DELETE')
        note = NoteBoard.objects.get(id=pk)
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def note_post(request):
    try:
        check_signed_in_request(request, method='POST')
        form = request.POST
        Level.validate_exists(form)
        fields = ['topic', 'text', 'level_id']
        noteUpdated = unserialize_note(form, fields=fields, optional=True)
    except RequestException as r:
        return r.jsonResponse
