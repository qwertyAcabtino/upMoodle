from rest.JSONResponse import JSONResponse
from rest.controllers.Exceptions.requestException import RequestExceptionByCode
from rest.controllers.controllers import check_signed_in_request
from rest.models import BannedHash
from rest.models.message.errorMessage import ErrorMessageType
from rest.orm.serializers import *
from rest.services.calendar import calendar_get_by_period, calendar_get, calendar_delete, calendar_put, \
    calendar_post
from rest.services.notes import note_get, note_delete, note_put, note_post, note_get_by_level

# noinspection PyUnresolvedReferences
from routers.file import *
# noinspection PyUnresolvedReferences
from routers.auth import *
# noinspection PyUnresolvedReferences
from routers.level import *
# noinspection PyUnresolvedReferences
from routers.rol import *
# noinspection PyUnresolvedReferences
from routers.user import *

@csrf_exempt
def bannedhashList(request):
    """
    Retrieves the banned file's hash list.
    """
    if request.method == 'GET':
        hashes = BannedHash.objects.all()
        serializer = BannedHashSerializer(hashes, many=True)
        return JSONResponse(serializer.data)


# == Notes ==
@csrf_exempt
def noteById(request, pk):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return note_get(request, pk)
        elif request.method == 'DELETE':
            return note_delete(request, pk)
        elif request.method == 'POST':
            return note_put(request, pk)
    except RequestException as r:
        return r.jsonResponse
    except OverflowError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse


@csrf_exempt
def note(request):
    try:
        check_signed_in_request(request)
        if request.method == 'POST':
            return note_post(request)
    except RequestException as r:
        return r.jsonResponse


def noteByLevel(request, level):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return note_get_by_level(request, level)
    except RequestException as r:
        return r.jsonResponse
    except OverflowError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse


# == Calendar ==
def calendarByPeriod(request, period, initDate):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return calendar_get_by_period(request, period, initDate)
    except RequestException as r:
        return r.jsonResponse
    except OverflowError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse


@csrf_exempt
def calendarById(request, pk):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return calendar_get(request, pk)
        elif request.method == 'DELETE':
            return calendar_delete(request, pk)
        elif request.method == 'POST':
            return calendar_put(request, pk)
    except RequestException as r:
        return r.jsonResponse
    except OverflowError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse


@csrf_exempt
def calendar(request):
    try:
        check_signed_in_request(request)
        if request.method == 'POST':
            return calendar_post(request)
    except RequestException as r:
        return r.jsonResponse