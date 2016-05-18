from django.views.decorators.csrf import csrf_exempt

from upmoodle.controllers.decorators.exceptions import zero_exceptions
from upmoodle.controllers.decorators.router import method, authenticated, methods
from upmoodle.models import OkMessage
from upmoodle.routers.response.factory import ResponseFactory
from upmoodle.services.file import FileService, FileTypeService


@zero_exceptions
@csrf_exempt
@authenticated
@methods(('GET', 'PUT', 'DELETE'))
def file_by_hash_endpoint(request, file_hash, session_token=None, data=None):

    def binary(file_hash_in=file_hash):
        file_obj = FileService.get_by_id(file_hash=file_hash_in)
        return ResponseFactory().ok().body(obj=file_obj).media_type(media_type='application/octet-stream').build()

    def delete(session_token=session_token, file_hash=file_hash, data=data):
        FileService.delete(session_token=session_token, file_hash=file_hash, data=data)
        return ResponseFactory().ok(message_id=OkMessage.Type.FILE_REMOVED).build()

    def metadata_update(session_token=session_token, file_hash=file_hash, data=data):
        FileService.metadata_update(session_token=session_token, file_hash=file_hash, data=data)
        return ResponseFactory().ok(message_id=OkMessage.Type.FILE_UPDATED).build()

    def get_by_id(session_token=session_token, file_hash=file_hash, data=data):
        file_in = FileService.get_by_id(session_token=session_token, file_hash=file_hash, data=data)
        return ResponseFactory().ok().body(obj=file_in).build()

    if request.method == 'DELETE' or _get_media_type(request) == 'application/json':
        return {
            'GET': get_by_id,
            'PUT': metadata_update,
            'DELETE': delete
        }[request.method](session_token=session_token, file_hash=file_hash, data=data)
    else:
        return binary(file_hash_in=file_hash)


@zero_exceptions
@csrf_exempt
@authenticated
@method('POST')
def file_add_endpoint(request, session_token=None, data=None):
    files = request.FILES
    new_file = FileService.add(session_token=session_token, data=data, files=files)
    new_file.id = new_file.hash
    return ResponseFactory().ok(message_id=OkMessage.Type.FILE_UPLOADED).identity(obj=new_file).build()


@zero_exceptions
@csrf_exempt
@authenticated
@method('GET')
def filetype_list(request, **kwargs):
    return ResponseFactory().ok().body(obj=FileTypeService.get()).build()


@zero_exceptions
@authenticated
@method('GET')
def files_banned_hashes(request, **kwargs):
    return ResponseFactory().ok().body(obj=FileService.get_banned_hashes()).build()


@zero_exceptions
@authenticated
@method('GET')
def user_related_files(request, session_token=None, **kwargs):
    files = FileService.get_user_latest(session_token=session_token, **kwargs)
    return ResponseFactory().ok().body(obj=files).build()


def _get_media_type(request):
    try:
        return request.META['HTTP_ACCEPT'].split(',')[0].lower()
    except:
        return request.META['CONTENT_TYPE'].split(',')[0].lower()
