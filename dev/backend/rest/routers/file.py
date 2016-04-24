from django.views.decorators.csrf import csrf_exempt

from rest.controllers.Exceptions.requestException import RequestExceptionByCode, RequestException
from rest.controllers.controllers import check_signed_in_request
from rest.models.message.errorMessage import ErrorMessageType
from rest.services.files import FileService


@csrf_exempt
def file_by_hash_endpoint(request, file_hash):

    try:
        check_signed_in_request(request)
        accept = request.META['HTTP_ACCEPT'].split(',')[0].lower()
        content_type = request.META['CONTENT_TYPE'].split(',')[0].lower()

        if 'application/json' == content_type or 'application/json' == accept:
            service_metadata_methods = {
                'GET': FileService.metadata_get,
                'PUT': FileService.metadata_update,
                'DELETE': FileService.delete
            }
            return service_metadata_methods[request.method](request, file_hash)
        else:
            service_binary_methods = {
                'GET': FileService.binary_get
            }
            return service_binary_methods[request.method](request, file_hash)

    except KeyError:
        return RequestExceptionByCode(ErrorMessageType.NOT_ALLOWED_METHOD).jsonResponse
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def file_add_endpoint(request):
    try:
        check_signed_in_request(request)
        if request.method == 'POST':
            return FileService.add(request)
        else:
            raise RequestException
    except RequestException as r:
        return r.jsonResponse
