from django.views.decorators.csrf import csrf_exempt

from rest.exceptions.requestException import RequestException
from rest.routers.decorators.routing_decorators import method, authenticated, methods
from rest.services.file import FileService, FileTypeService


@csrf_exempt
@authenticated
@methods(('GET', 'PUT', 'DELETE'))
def file_by_hash_endpoint(request, file_hash, session_token=None, data=None):
    try:
        accept = request.META['HTTP_ACCEPT'].split(',')[0].lower()
        content_type = request.META['CONTENT_TYPE'].split(',')[0].lower()

        if 'application/json' == content_type or 'application/json' == accept:
            service_metadata_methods = {
                'GET': FileService.metadata_get,
                'PUT': FileService.metadata_update,
                'DELETE': FileService.delete
            }
            return service_metadata_methods[request.method](session_token=session_token, file_hash=file_hash, data=data)
        else:
            service_binary_methods = {
                'GET': FileService.binary_get
            }
            return service_binary_methods[request.method](file_hash=file_hash)

    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
@authenticated
@method('POST')
def file_add_endpoint(request, session_token=None, data=None):
    files = request.FILES
    return FileService.add(session_token=session_token, data=data, files=files)


@authenticated
@method('GET')
def filetype_list(request, **kwargs):
    return FileTypeService.get()


@authenticated
@method('GET')
def files_banned_hashes(request, **kwargs):
    return FileService.get_banned_hashes()
