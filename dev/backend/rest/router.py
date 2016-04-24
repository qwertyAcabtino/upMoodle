from django.core.exceptions import ObjectDoesNotExist

from rest.JSONResponse import JSONResponse
from rest.models import BannedHash, Rol, File, Level, User
from rest.orm.serializers import *
from rest.orm.serializers.rol import RolSerializer
from rest.services.calendar import calendar_get_by_period, calendar_get, calendar_delete, calendar_put, \
    calendar_post
from rest.services.notes import note_get, note_delete, note_put, note_post, note_get_by_level
from rest.services.system import recoverPassword_sys, \
    subjectsTree_get, fileTypes_get, confirmEmail_sys
from rest.services.users import user_get, user_delete, user_put, user_get_id, user_get_rol, user_subjects_put, \
    user_put_profile_pic

# noinspection PyUnresolvedReferences
from routers.file import *
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


@csrf_exempt
def usersList(request):
    """
    Retrieves an user's list.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def rolesList(request):
    """
    Retrieves an user's list filtered by rol.
    """
    if request.method == 'GET':
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return JSONResponse(serializer.data)


def filesList(request):
    """
    Retrieves a file's list .
    """
    if request.method == 'GET':
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return JSONResponse(serializer.data)


def fileListSubject(request, pk):
    level = Level.objects.get(id=pk)
    if level.is_subject() and request.method == 'GET':
        files = File.objects.filter(subject=pk, visible=True)
        serializer = FileSerializer(files, many=True)
        return JSONResponse(serializer.data)
    elif not level.is_subject():
        return RequestExceptionByCode(ErrorMessageType.INVALID_LEVEL).jsonResponse


# Final APIS.
# == System APIs ==

@csrf_exempt
def confirmEmail(request):
    return confirmEmail_sys(request)


@csrf_exempt
def recoverPassword(request):
    return recoverPassword_sys(request)


# == Users ==
@csrf_exempt
def user(request):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return user_get(request)
        elif request.method == 'DELETE':
            return user_delete(request)
        elif request.method == 'POST':
            return user_put(request)
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def user_subjects(request):
    try:
        check_signed_in_request(request)
        if request.method == 'POST':
            return user_subjects_put(request)
    except RequestException as r:
        return r.jsonResponse

@csrf_exempt
def user_profilepic(request):
    try:
        check_signed_in_request(request)
        if request.method == 'POST':
            return user_put_profile_pic(request)
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def userById(request, pk):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return user_get_id(request, pk)
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def usersByRol(request, pk):
    return user_get_rol(request, pk)


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




def subjectsTree(request):
    try:
        check_signed_in_request(request, 'GET')
        return subjectsTree_get()
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist or OverflowError or ValueError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse


def fileTypes(request):
    try:
        check_signed_in_request(request, 'GET')
        return fileTypes_get()
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist or OverflowError or ValueError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
