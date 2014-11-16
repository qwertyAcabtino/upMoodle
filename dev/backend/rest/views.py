from django.core.mail import send_mail
from django.utils.datastructures import MultiValueDictKeyError

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from backend import settings
from rest.ERROR_MESSAGE_ID import INCORRECT_DATA, REQUEST_CANNOT, DISABLED_COOKIES, INVALID_TOKEN, ALREADY_CONFIRMED

from rest.JSONResponse import JSONResponse
from rest.requestException import RequestExceptionByMessage, RequestExceptionByCode
from rest.serializers import *
from rest.unserializers import unserialize_user
from rest.utils import get_email_confirmation_message


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
def noteboardNote(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        note = NoteBoard.objects.get(pk=pk)
    except NoteBoard.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NoteBoardSerializer(note)
        return JSONResponse(serializer.data)


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
def usersByRol(request, pk):
    """
    Retrieves an user's list filtered by rol.
    """
    if request.method == 'GET':
        users = User.objects.filter(rol=pk)
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
    # Todo. Restrict to logged user.
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


@csrf_exempt
def login(request):
    # engine = import_module(settings.SESSION_ENGINE)
    # session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    try:
        if request.method == 'POST':
            try:
                session_key = request.session.session_key
                emailIn = request.POST['email']
                passwordIn = request.POST['password']
                try:
                    user = User.objects.get(email=emailIn, password=passwordIn)
                except ObjectDoesNotExist:
                    raise Exception('Incorrect sign in values')
                user.sessionToken = session_key
                user.save()
                message = Message()
                message.message = 'Successfully signed in.'
                serializer = MessageSerializer(message, many=False)
                jsonResponse = JSONResponse(serializer.data, status=201)

                jsonResponse.set_cookie(settings.SESSION_COOKIE_NAME, session_key)
                return jsonResponse
            except Exception as e:
                error = ErrorMessage()
                error.error = e.message
                serializer = ErrorMessageSerializer(error, many=False)
                return JSONResponse(serializer.data, status=400)
        else:
            raise RequestExceptionByMessage(INCORRECT_DATA)
    except RequestExceptionByMessage as r:
        return r.jsonResponse


# Final APIS.

@csrf_exempt
def signup(request):
    try:
        if not request.session.test_cookie_worked():
            return RequestExceptionByCode(DISABLED_COOKIES).jsonResponse
        elif request.method == 'POST':
            user = unserialize_user(request.POST, request.COOKIES['cruasanPlancha'])
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
    except MultiValueDictKeyError as m:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


def confirmEmail(request, cookie):
    try:
        if request.method == 'GET':
            user = User.objects.get(sessionToken=cookie)
            if not user.banned:
                return RequestExceptionByCode(ALREADY_CONFIRMED).jsonResponse
            else:
                user.banned = False
                user.save()
                return JSONResponse({"userId": user.id}, status=200)
        else:
            return RequestExceptionByCode(REQUEST_CANNOT).jsonResponse
    except ObjectDoesNotExist as o:
        return RequestExceptionByCode(INVALID_TOKEN).jsonResponse
