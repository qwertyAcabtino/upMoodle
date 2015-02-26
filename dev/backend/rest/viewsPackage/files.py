from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from backend.settings import SESSION_COOKIE_NAME_BIS
from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.MESSAGES_ID import INCORRECT_DATA, NOTE_REMOVED, FILE_REMOVED
from rest.controllers.Exceptions.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from rest.controllers.controllers import check_signed_in_request, check_authorized_author
from rest.models import File, NoteBoard, Level, User
from rest.orm.serializers import FileSerializer
from rest.orm.unserializers import unserialize_file


def file_get_info(request, pk):
    try:
        check_signed_in_request(request, 'GET')
        files = File.objects.filter(id=pk, visible=True)
        serializer = FileSerializer(files, many=True)
        jsonResponse = JSONResponse(serializer.data)
        return jsonResponse
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist or OverflowError or ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


def file_get_binary(request, pk):
    try:
        check_signed_in_request(request, 'GET')
        file = File.objects.get(id=pk)
        path_to_file = file.file.path

        extension = file.extension()
        f = open(path_to_file, 'r')
        myfile = File(f)
        response = HttpResponse(file.file)
        response['Content-Disposition'] = 'attachment; filename=' + file.name + '.' + extension
        return response
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist or OverflowError or ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse

@csrf_exempt
def file_put(request, pk):
    try:
        fileOriginal = File.objects.get(id=pk)

        check_signed_in_request(request, method='POST')
        check_authorized_author(request, fileOriginal.uploader_id, level=True)

        form = request.POST
        Level.validate_exists_level(form['subject'])
        fields = ['topic', 'text', 'level_id']
        note = unserialize_file(form, fields=fields, optional=True)
        note.lastUpdater_id = User.get_signed_user_id(request.COOKIES[SESSION_COOKIE_NAME_BIS])
        note.save()
        return JSONResponse({"noteId": note.id}, status=200)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except ValidationError as v:
        return RequestExceptionByMessage(v).jsonResponse

@csrf_exempt
def file_delete(request, pk):
    try:
        check_signed_in_request(request, method='DELETE')
        model = File.objects.get(id=pk)
        check_authorized_author(request, model.uploader_id, same=True)
        model.visible = False
        model.save()
        return JSONResponseID(FILE_REMOVED)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse

@csrf_exempt
def file_post(request, pk):
    pass
    # TODO