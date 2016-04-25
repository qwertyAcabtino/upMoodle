from django.views.decorators.csrf import csrf_exempt

from rest.JSONResponse import JSONResponse
from rest.controllers.Exceptions.requestException import RequestExceptionByCode, RequestException
from rest.controllers.controllers import check_signed_in_request
from rest.models import BannedHash
from rest.models.message.errorMessage import ErrorMessageType
from rest.orm.serializers import *
from rest.services.calendar import calendar_get_by_period, calendar_get, calendar_delete, calendar_put, \
    calendar_post

# noinspection PyUnresolvedReferences
from routers.auth import *

@csrf_exempt
def bannedhashList(request):
    """
    Retrieves the banned file's hash list.
    """
    if request.method == 'GET':
        hashes = BannedHash.objects.all()
        serializer = BannedHashSerializer(hashes, many=True)
        return JSONResponse(serializer.data)

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