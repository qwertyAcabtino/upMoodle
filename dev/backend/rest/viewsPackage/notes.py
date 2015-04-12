from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.csrf import csrf_exempt
import time
from backend.settings import SESSION_COOKIE_NAME_BIS
from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.MESSAGES_ID import INCORRECT_DATA, NOTE_UPDATED, NOTE_REMOVED
from rest.controllers.Exceptions.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from rest.controllers.controllers import check_signed_in_request, check_authorized_author
from rest.models import NoteBoard, Level, User
from rest.orm.serializers import NoteBoardSerializer
from rest.orm.unserializers import unserialize_note
from rest.viewsPackage.system import subjectsTree_get_ids


@csrf_exempt
def note_get(request, pk):
    try:
        check_signed_in_request(request, 'GET')
        note = NoteBoard.objects.get(id=pk, visible=True)
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
        check_authorized_author(request, noteOriginal.author_id, level=True)

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
def note_delete(request, pk):
    try:
        check_signed_in_request(request, method='DELETE')
        note = NoteBoard.objects.get(id=pk)
        check_authorized_author(request, note.author_id, same=True)
        note.visible = False
        note.save()
        return JSONResponseID(NOTE_REMOVED)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse

@csrf_exempt
def note_post(request):
    try:
        check_signed_in_request(request, method='POST')
        form = request.POST
        Level.validate_exists(form)
        fields = ['topic', 'text', 'level_id']
        note = unserialize_note(form, fields=fields, optional=True)
        note.author_id = User.get_signed_user_id(request.COOKIES[SESSION_COOKIE_NAME_BIS])
        note.save()
        return JSONResponse({"noteId": note.id}, status=200)
    except RequestException as r:
        return r.jsonResponse
    except ValidationError as v:
        return RequestExceptionByMessage(v).jsonResponse


def note_get_by_level(request, level):
    try:
        check_signed_in_request(request, method='GET')
        Level.validate_exists_level(level)
        level_group = (level, 2)
        form = request.GET
        if form['recursive'] and form['recursive']=='true':
            level_group = subjectsTree_get_ids(level)
        else:
            level_group = (level,)
        note = NoteBoard.objects.filter(level_id__in=level_group, visible=True)
        serializer = NoteBoardSerializer(note, many=True)
        return JSONResponse(serializer.data)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except OverflowError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
