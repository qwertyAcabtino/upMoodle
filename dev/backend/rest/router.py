from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from backend import settings
from backend.settings import SESSION_COOKIE_NAME, SESSION_COOKIE_NAME_BIS
from rest.MESSAGES_ID import INCORRECT_DATA, REQUEST_CANNOT, DISABLED_COOKIES, INVALID_TOKEN, ALREADY_CONFIRMED, \
    SUCCESS_LOGIN, UNCONFIRMED_EMAIL, RECOVER_PASS_EMAIL, UNAUTHORIZED, USER_REMOVED, USER_UPDATED, NOTE_UPDATED
from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.controllers.Exceptions.requestException import RequestExceptionByMessage, RequestExceptionByCode, \
    RequestException
from rest.orm.serializers import *
from rest.controllers.controllers import get_email_confirmation_message, cookies_are_ok, send_recover_password_email, \
    get_random_password, \
    get_random_email, check_signed_in_request, check_cookies, check_authorized_author
from rest.orm.unserializers import unserialize_user, unserialize_note
from rest.viewsPackage.calendar import calendar_get_by_period, calendar_get, calendar_delete, calendar_put, \
    calendar_post
from rest.viewsPackage.files import file_get_info, file_get_binary, file_put, file_delete, file_post
from rest.viewsPackage.notes import note_get, note_delete, note_put, note_post, note_get_by_level
from rest.viewsPackage.system import signup_sys, confirmEmail_sys, login_sys, logout_sys, recoverPassword_sys, \
    subjectsTree_get, fileTypes_get
from rest.viewsPackage.users import user_get, user_delete, user_put, user_get_id, user_get_rol, user_subjects_put, \
    user_put_profile_pic


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


# Final APIS.
# == System APIs ==
@csrf_exempt
def signup(request):
    return signup_sys(request)


def confirmEmail(request, cookie):
    return confirmEmail_sys(request, cookie)


@csrf_exempt
def login(request):
    return login_sys(request)


@csrf_exempt
def logout(request):
    return logout_sys(request)


@csrf_exempt
def recoverPassword(request):
    return recoverPassword_sys(request)


# == Users ==
@csrf_exempt
def user(request):
    try:
        check_signed_in_request(request)
        print request.method
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
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


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
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


# == Calendar ==
def calendarByPeriod(request, period, initDate):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return calendar_get_by_period(request, period, initDate)
    except RequestException as r:
        return r.jsonResponse
    except OverflowError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


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
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


@csrf_exempt
def calendar(request):
    try:
        check_signed_in_request(request)
        if request.method == 'POST':
            return calendar_post(request)
    except RequestException as r:
        return r.jsonResponse


# == Files ==
@csrf_exempt
def fileById(request, pk):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return file_get_info(request, pk)
        if request.method == 'POST':
            return file_put(request, pk)
        if request.method == 'DELETE':
            return file_delete(request, pk)
    except RequestException as r:
        return r.jsonResponse

@csrf_exempt
def fileBinary(request, pk):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return file_get_binary(request, pk)
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def file_binary(request):
    try:
        check_signed_in_request(request)
        if request.method == 'POST':
            return file_post(request)
        else:
            raise RequestException
    except RequestException as r:
        return r.jsonResponse


def subjectsTree(request):
    try:
        check_signed_in_request(request, 'GET')
        return subjectsTree_get()
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist or OverflowError or ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


def fileTypes(request):
    try:
        check_signed_in_request(request, 'GET')
        return fileTypes_get()
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist or OverflowError or ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
