from django.views.decorators.csrf import csrf_exempt

from upmoodle.models.utils.requestException import RequestException
from upmoodle.routers.decorators.routing_decorators import method, authenticated, methods, response
from upmoodle.services.file import FileService, FileTypeService


@csrf_exempt
@authenticated
@methods(('GET', 'PUT', 'DELETE'))
def file_by_hash_endpoint(request, file_hash, session_token=None, data=None):

    @response(media_type='application/octet-stream')
    def binary(file_hash_in=file_hash):
        return FileService.get_by_id(file_hash=file_hash_in)

    @response(media_type='application/json')
    def metadata(session_token=session_token, file_hash=file_hash, data=data):
        service_metadata_methods = {
            'GET': FileService.get_by_id,
            'PUT': FileService.metadata_update,
            'DELETE': FileService.delete
        }
        return service_metadata_methods[request.method](session_token=session_token, file_hash=file_hash, data=data)

    try:
        if request.method == 'DELETE' or _get_media_type(request) == 'application/json':
            return metadata(session_token=session_token, file_hash=file_hash, data=data)
        else:
            return binary(file_hash_in=file_hash)

    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
@authenticated
@method('POST')
@response(media_type='application/json')
def file_add_endpoint(request, session_token=None, data=None):
    files = request.FILES
    return FileService.add(session_token=session_token, data=data, files=files)


@authenticated
@method('GET')
@response(media_type='application/json')
def filetype_list(request, **kwargs):
    return FileTypeService.get()


@authenticated
@method('GET')
@response(media_type='application/json')
def files_banned_hashes(request, **kwargs):
    return FileService.get_banned_hashes()


def _get_media_type(request):
    try:
        return request.META['HTTP_ACCEPT'].split(',')[0].lower()
    except:
        return request.META['CONTENT_TYPE'].split(',')[0].lower()
