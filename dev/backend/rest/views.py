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

@csrf_exempt
def noteboardList(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        notes = NoteBoard.objects.all()
        serializer = NoteBoardSerializer(notes, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NoteBoardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def noteboardLevel(request, pk):
    """
    Retrieves the noteboards from a level.
    """
    if request.method == 'GET':
        notes = NoteBoard.objects.filter(level=pk)
        serializer = NoteBoardSerializer(notes, many=True)
        return JSONResponse(serializer.data)


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


@csrf_exempt
def calendarList(request):
    """
    Retrieves user's future calendar events.
    """
    if request.method == 'GET':
        events = CalendarRegularEvent.objects.all()
        serializer = CalendarEventSerializer(events, many=True)
        return JSONResponse(serializer.data)


def filesList(request):
    """
    Retrieves a file's list .
    """
    if request.method == 'GET':
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return JSONResponse(serializer.data)


def file(request, pk):
    """
    Retrieves a file information.
    """
    if request.method == 'GET':
        files = File.objects.filter(id=pk)
        serializer = FileSerializer(files, many=True)
        return JSONResponse(serializer.data)


def fileBinary(request, pk):
    file = File.objects.get(id=pk)
    path_to_file = file.file.path

    extension = file.extension()
    f = open(path_to_file, 'r')
    myfile = File(f)
    response = HttpResponse(file.file)
    response['Content-Disposition'] = 'attachment; filename=' + file.name + '.' + extension
    return response


def fileListSubject(request, pk):
    level = Level.objects.get(id=pk)
    if level.is_subject() and request.method == 'GET':
        files = File.objects.filter(subject=pk)
        serializer = FileSerializer(files, many=True)
        return JSONResponse(serializer.data)


# Final APIS.

@csrf_exempt
def signup(request):
    try:
        check_cookies(request)
        if request.method == 'POST':
            user = unserialize_user(request.POST, sessionToken=request.COOKIES[SESSION_COOKIE_NAME],
                                    fields=['email', 'password', 'nick'])
            send_mail('Email confirmation',
                      get_email_confirmation_message(request),
                      'info@upmoodle.com', [user.email],
                      fail_silently=False)
            user.save()
            return JSONResponse({"userId": user.id}, status=200)
        else:
            return RequestExceptionByCode(REQUEST_CANNOT).jsonResponse
    except ValidationError as v:
        r = RequestExceptionByMessage(v)
        return r.jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except RequestException as r:
        return r.jsonResponse

def confirmEmail(request, cookie):
    try:
        if request.method == 'GET':
            user = User.objects.get(sessionToken=cookie)
            if user.confirmedEmail:
                return RequestExceptionByCode(ALREADY_CONFIRMED).jsonResponse
            else:
                user.confirmedEmail = True
                user.save()
                return JSONResponse({"userId": user.id}, status=200)
        else:
            return RequestExceptionByCode(REQUEST_CANNOT).jsonResponse
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INVALID_TOKEN).jsonResponse


@csrf_exempt
def login(request):
    try:
        if not cookies_are_ok(request):
            return RequestExceptionByCode(DISABLED_COOKIES).jsonResponse
        elif request.method == 'POST':
            session_key = request.COOKIES[SESSION_COOKIE_NAME]
            emailIn = request.POST['email']
            passwordIn = request.POST['password']
            user = User.objects.get(email=emailIn, password=passwordIn)
            if not user.confirmedEmail:
                return RequestExceptionByCode(UNCONFIRMED_EMAIL).jsonResponse
            else:
                user.sessionToken = session_key
                user.lastTimeActive = timezone.now()
                user.save()
                message = Message.objects.get(pk=SUCCESS_LOGIN)
                serializer = MessageSerializer(message, many=False)
                jsonResponse = JSONResponse(serializer.data, status=200)
                jsonResponse.set_cookie(settings.SESSION_COOKIE_NAME, session_key)
                jsonResponse.set_cookie(settings.SESSION_COOKIE_NAME_BIS, session_key)
                return jsonResponse
        else:
            raise RequestExceptionByCode(REQUEST_CANNOT)
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def logout(request):
    try:
        if not cookies_are_ok(request):
            return RequestExceptionByCode(DISABLED_COOKIES).jsonResponse
        elif request.method == 'POST':
            session_key = request.COOKIES[SESSION_COOKIE_NAME_BIS]
            user = User.objects.get(sessionToken=session_key)
            user.sessionToken = ''
            user.save()
            jsonResponse = JSONResponse({"null"}, status=200)
            jsonResponse.delete_cookie(SESSION_COOKIE_NAME)
            jsonResponse.delete_cookie(SESSION_COOKIE_NAME_BIS)
            return jsonResponse
        else:
            raise RequestExceptionByCode(REQUEST_CANNOT)
    except Exception:
        return JSONResponse({"null"}, status=200)


@csrf_exempt
def recoverPassword(request):
    try:
        if request.method == 'POST':
            emailRequest = request.POST['email']
            user = User.objects.get(email=emailRequest)
            if not user.confirmedEmail:
                raise RequestExceptionByCode(UNCONFIRMED_EMAIL)
            elif user.banned:
                raise RequestExceptionByCode(UNAUTHORIZED)
            else:
                password = get_random_password()
                send_recover_password_email(user.email, password)
                user.password = password
                user.save()
                message = Message.objects.get(pk=RECOVER_PASS_EMAIL)
                serializer = MessageSerializer(message, many=False)
                jsonResponse = JSONResponse(serializer.data, status=200)
                return jsonResponse
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except RequestException as r:
        return r.jsonResponse


#TODO. POST and DELETE USER if permission
@csrf_exempt
def userThird(request, pk):
    try:
        check_signed_in_request(request, 'GET')
        users = User.objects.get(id=pk)
        serializer = UserSerializer(users, many=False)
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
def getUserSelf(request):
    try:
        check_signed_in_request(request, 'GET')
        sessionToken = request.COOKIES[SESSION_COOKIE_NAME_BIS]
        users = User.objects.get(sessionToken=sessionToken)
        serializer = UserSerializer(users, many=False)
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
def usersByRol(request, pk):
    try:
        check_signed_in_request(request, 'GET')
        users = User.objects.filter(rol=pk, banned=False)
        serializer = UserSerializer(users, many=True)
        return JSONResponse(serializer.data)
    except RequestException as r:
        return r.jsonResponse
    except OverflowError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


@csrf_exempt
def userRemove(request):
    try:
        check_signed_in_request(request, method='DELETE')
        sessionToken = request.COOKIES[SESSION_COOKIE_NAME_BIS]
        userSigned = User.objects.get(sessionToken=sessionToken)
        userSigned.name = 'RemovedUser ' + str(userSigned.id)
        userSigned.nick = 'RemovedUser ' + str(userSigned.id)
        userSigned.email = get_random_email()
        userSigned.password = get_random_password()
        userSigned.profilePic = '_default.png'
        userSigned.banned = True
        userSigned.confirmedEmail = False
        userSigned.save()
        message = Message.objects.get(pk=USER_REMOVED)
        serializer = MessageSerializer(message, many=False)
        jsonResponse = JSONResponse(serializer.data, status=200)
        return jsonResponse
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def userUpdate(request):
    try:
        check_signed_in_request(request, 'POST')
        form = request.POST
        userSigned = User.objects.get(sessionToken=request.COOKIES[SESSION_COOKIE_NAME_BIS])
        try:
            password = form['password']
            if not userSigned.password == form['oldPassword']:
                raise RequestExceptionByCode(INCORRECT_DATA)
        except MultiValueDictKeyError:
            pass
        fields = ['nick', 'name', 'password', 'email']
        userUpdated = unserialize_user(form, fields=fields, optional=True)
        userSigned.update(userUpdated, fields)
        userSigned.save()
        message = Message.objects.get(pk=USER_UPDATED)
        serializer = MessageSerializer(message, many=False)
        jsonResponse = JSONResponse(serializer.data, status=200)
        return jsonResponse
    except RequestException as r:
        return r.jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


@csrf_exempt
def user(request):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return getUserSelf(request)
        elif request.method == 'DELETE':
            return userRemove(request)
        elif request.method == 'POST':
            return userUpdate(request)
    except RequestException as r:
        return r.jsonResponse


# == Notes ==
@csrf_exempt
def noteboardNote(request, pk):
    try:
        check_signed_in_request(request)
        if request.method == 'GET':
            return note_get(request, pk)
        elif request.method == 'DELETE':
            return note_remove(request)
        elif request.method == 'POST':
            return note_update(request, pk)
    except RequestException as r:
        return r.jsonResponse

@csrf_exempt
def note_get(request, pk):
    try:
        check_signed_in_request(request, 'GET')
        note = NoteBoard.objects.get(id=pk)
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
def note_update(request, pk):
    try:
        noteOriginal = NoteBoard.objects.get(id=pk)

        check_signed_in_request(request, 'POST')
        check_authorized_author(request, noteOriginal.author_id)

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
def note_remove(request, pk):
    try:
        check_signed_in_request(request, method='DELETE')
        note = NoteBoard.objects.get(id=pk)
    except RequestException as r:
        return r.jsonResponse

# """
# Retrieve, update or delete a code snippet.
# """
#     try:
#         note = NoteBoard.objects.get(pk=pk)
#     except NoteBoard.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = NoteBoardSerializer(note)
#         return JSONResponse(serializer.data)
#
